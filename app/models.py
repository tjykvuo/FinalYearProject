import io
import re
import csv
import json
from django.db import models
from django.db.models.signals import pre_save, post_save 
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError, ImproperlyConfigured 
from django.core.validators import MaxValueValidator
from model_utils.managers import InheritanceManager 
from .uploadsig import upload_csv
from .validator import csv_file_validator_function

# Create your models here.
class Post(models.Model):
    #the post model forms part of the blog; this was added 
    #to increase the artefact's capabilities
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True, null=True)
    
    def publish(self):#blog publishing
      self.publishing_date=timezone.now()
      self.save()
  
    def __stf__(self):
      return self.title

class Person(models.Model):
    class Meta:
        permissions = [('can_view_content', 'Can view content')]

class QuizTypeManager(models.Manager):
    #QuizTypeManager directs how the QuizType model
    #will be controlled
    def new_quiz_type(self, quiztype):
        new_quiz_type = self.create(quiztype=re.sub('\s+','-', quiztype) 
                                    .lower())
        new_quiz_type.save()
        return new_quiz_type

 
class QuizType(models.Model):
# QuizType is specifying which type of quiz will be used, 
# it is largely applied for future topic expansion. 
    quiztype=models.CharField(
        verbose_name=_("Quiz Type"), 
        max_length=250, blank=True,
        unique=True, null=True)
    objects = QuizTypeManager()
    class Meta:
        verbose_name=_("Quiz Type")
        verbose_name_plural=_("Quiz Types")
        #verbose field names are optionally used to increase readability
        #verbose plural are used to pluralise field statements to make them more readable 
        def __str__(self):
            return self.quiztype


class Quiz(models.Model):#the Quiz model is applied to detail the makeup of the quizzes
    title=models.CharField(
        verbose_name=_("Title"),
        max_length=60, blank=False)

    descriptor=models.TextField(
        verbose_name=_("Quiz Description"),
        blank=True, help_text=_("Useful information about the quiz"))

    url=models.SlugField(
        max_length=60, blank=False,
        help_text=_("a useful url"),
        verbose_name=_("a compatible url that is user friendly"))

    quiztype = models.ForeignKey(
        QuizType, null=True, blank=True,
        verbose_name=_("Quiz Type"), on_delete=models.CASCADE)

    variable_order=models.BooleanField(
        blank=False, default=False,
        verbose_name=_("Variable Order"),
        help_text=_("Questions are displayed in random to prevent cheating"))

    attempt_record =models.BooleanField(
        blank=False, default=False,
        help_text=_("if active; the result from an attempt will be recorded"),
        verbose_name=_("Quiz Attempt Record"))

    max_questions = models.PositiveIntegerField(
        blank = True,
        null = True,
        verbose_name=_("Maximum questions"),
        help_text=_("Number of questions to be answered"))

    answers_at_end = models.BooleanField(
        blank = False, 
        default = False, 
        help_text=_("Answers displayed at end of quiz"),
        verbose_name=_("Answers shown at end"))

    one_quiz_effort = models.BooleanField(
        blank=False, default=False,
        help_text=_("If active, users can only have one attempt at quiz"
                    "so that users will not be able to cheat"))

    quiz_pass_mark=models.SmallIntegerField(
        blank=True, default=0,
        verbose_name=_("Mark"),
        help_text=_("Mark required to pass the quiz"),
        validators=[MaxValueValidator(10)])

    quiz_pass_notif=models.TextField(
        blank=True, help_text=_("Display if user passes quiz"),
        verbose_name=_("Pass Notification"))

    quiz_fail_notif=models.TextField(
        blank=True, help_text=_("Display if user fails to pass quiz."),
        verbose_name=_("Fail Notification"))

    quiz_outline = models.TextField(
        blank=True, default=False,
        verbose_name=_("Rough Outline"), 
        help_text=_("If active; only authorised users will be able to take the quiz"
                    "as it will not be displayed in the Quiz List. Only users with"
                    "quiz edit permissions may gain access."))

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        self.url = re.sub('\s+', '-', self.url).lower()
        self.url=''.join(letter for letter 
                         in self.url 
                         if letter.isalnum() or letter == '-' )
        if self.one_quiz_effort is True:
            self.attempt_record = True
        if self.quiz_pass_mark > 10:
           raise ValidationError('%s is above 7' % self.quiz_pass_mark)
        super(Quiz, self).save(force_insert, force_update, *args, **kwargs)

        class Meta:
            verbose_name=_("Quiz")
            verbose_name_plural=_("Quizzes")

        def __str__(self):
            return self.title

        def get_questions(self):
            return self.question_set.all().select_subclasses()

        @property
        def show_max_mark(self):
            return self.get_questions().count()

        def anon_quiz_list(self):
            return str(self.id) + "_q_list"

        def score_id(self):
            return str(self.id) + "_score"

        def quiz_data(self):
            return str(self.id) + "_data"


class QuizCBMController(models.Manager):#serves as progress monitor management
    def new_progress(self, user):
        new_progress=self.create(user=user, score="")
        new_progress.save()
        return new_progress

class QuizCBM(models.Model):
#CBM (Curriculum Based Measurement) is a progression metric
#which aims to determine a users performance
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("User"), 
        on_delete=models.CASCADE)
    result=models.CharField(
       max_length=1024,
        verbose_name=_("Result"))
    right_answer=models.CharField(
        max_length=10, 
        verbose_name=_('Right Answer'))
    wrong_answer=models.CharField(
        max_length=10,
        verbose_name=_('Wrong Answer'))
    objects=QuizCBMController()

    class Meta:
        verbose_name=_("Quiz Progression")

    @property
    def displayQuizTypeScores(self): #displays scores by quiztype
        result_before=self.result
        output={}

        for qtype in QuizType.objects.all():
            to_find = re.escape(qtype.quiztype) + r", (\d+),(\d+),"

            match = re.search(to_find, self.result, re.IGNORECASE)

            if match:
                result = int(match.group(1))
                possible = int(match.group(2))

                try:
                    percent = int(round((float(result)/ float (possible))* 100))
                except:
                    percent = 0
                output[qtype.quiztype] = [result, possible, percent]
            
            else: self.result += qtype.quiztype + ",0,0,"
            output[qtype.quiztype] = [0, 0]

        if len(self.result) > len(result_before):
            self.save()
        return output

    def update_result(self, question, result_to_add=0, possible_to_add=0): #display user results at the end of the quiz
        quiztype_test = QuizType.objects.filter(quiztype=question.quiztype).exists()

        if any([item is False for item in [quiztype_test,
                                           result_to_add,
                                           possible_to_add,
                                           isinstance(score_to_add, int),
                                           isinstance(possible_to_add, int)]]):
            return _("error"), _("quiztype does not exist or is invalid")

        to_find = re.escape(str(question.quiztype)) + r",(?P<result>\d+),(?P<possible>\d+),"
        match = re.search(to_find, self.result, re.IGNORECASE)

        if match:
            updated_result = int(match.group('score')) + abs(result_to_add)
            updated_possible = int(match.group('possible'))+ abs(possible_to_add)

            new_score = ";".join(
                [
                    str(question.quiztype),
                    str(updated_result),
                    str(updated_possible), ""
                    ]
                )
            self.result = self.result.replace(match.group(), new_result)
            self.result()
        else:
            self.result += ";".join(
                [
                    str(question.quiztype),
                    str(score_to_add),
                    str(possible_to_add), ""
                    ]
                )
            self.save()
    
    def display_attempts(self):#displays the number of quiz attempts that a participant has made
       return Attempt.objects.filter(
           user=self.user, 
           completed_attempt=True)

    def __str__(self):
       return self.user.username + '-' + self.result


class AttemptManager(models.Manager):
#AttemptManager is responsible for controlling how users access quizzes
#and whether they are able to make multiple attempts. for the purpose of
#this research exercise users will only be permitted one attempt per quiz.

    def new_attempt(self, user, quiz):
        if quiz.variable_order is True:
            question_set = quiz.question_set.all().select_subclasses().order_by('?')
        else:
            question_set = quiz.question_set.all().select_subclasses()

        question_set=[item.id for item in question_set]

        if len(question_set) == 0:
            raise ImproperlyConfigured('Question set is empty'
                                       'Please configure quiz correctly')
        if quiz.max_questions and quiz.max_questions < len(question_set):
            question_set=question_set[: quiz.max_questions]
            
            questions=",".join(map(str, question_set)) + ","

            new_attempt = self.create(user=user, 
                                      quiz=quiz, 
                                      question_order=questions,
                                      question_list=questions,
                                      wrong_response="",
                                      present_score=0, 
                                      completed_attempt=False, 
                                      participant_answers='{}')
            return new_attempt

    def user_attempt(self, user, quiz):
        if quiz.one_quiz_effort is True and self.filter(user=user,
                                                            quiz=quiz,
                                                            completed_attempt=True).exists():
                return False
        try:
                attempt = self.get(user=user, quiz=quiz, completed_attempt=False)
        except Attempt.DoesNotExist:
                attempt = self.new_attempt(user, quiz)
        except Attempt.MultipleObjectsReturned:
                attempt = self.filter(user=user, 
                                      quiz=quiz, 
                                      completed_attempt=False)[0]
        return attempt


class Attempt(models.Model): 
#the attempt model handles metrics on the user's attempt
#and how they did when they sat the quiz
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("User"),
        on_delete=models.CASCADE)
    quiz=models.ForeignKey(
        Quiz, verbose_name=_("Quiz"),
        on_delete=models.CASCADE)
    question_order=models.CharField(
        max_length=1024, 
        verbose_name=_("Question Order"))
    question_list=models.CharField(
        max_length=1024, 
        verbose_name=_("Question List"))
    wrong_questions=models.CharField(
        max_length=1024, 
        blank=True, 
        verbose_name=_("Wrong Questions"))
    present_score=models.IntegerField(
        verbose_name=_("Present Score"))
    completed_attempt=models.BooleanField(
        default=False, 
        blank=False, 
        verbose_name=_("Completed Attempt"))
    participant_answers = models.TextField(
       blank=True,
      default='{}', 
      verbose_name=_("Answers From Test Participants"))

    attempt_start = models.DateTimeField(auto_now_add=True, verbose_name=_("Start of Attempt"))
    
    attempt_end = models.DateTimeField(auto_now_add=True, verbose_name=_("End of Attempt"))

    objects = AttemptManager()

    class Meta:
        permissions=(("view_attempts", _("can see completed quizzes")),)

    #get_first_question determines which question comes first
    def get_first_question(self):
        if not self.question_list:
            return False
        first, _ = self.question_list.split(',', 1)
        question_id = int(first)
        return Question.objects.get_subclass(id=question_id)
    #remove question from first position
    def remove_first_question(self):
        if not self.question_list:
            return
        _, others = self.question_list.split(',', 1)
        self.question_list = others
        self.save()
    #is used to update scores however as users will only get one attempt
    #add_to_score is not required and included for system completeness
    def add_to_score(self, points):
        self.present_score += int(points)
        self.save()

    @property 
    def get_present_score(self): #returns the user's score which has been determined by answering questions
        return self.present_score
    
    def _question_ids(self): #question_id uniquely udentifies each question being proposed to the user 
        return[int(n) for n in self.question_order.split(',') if n] 

    @property
    def get_score_percentage(self): #returns the user's score percentage based on their performance
        dividend = float(self.present_score)
        divisor = len(self._question_ids())
        if divisor < 1:
            return 0
        if dividend > divisor:
            return 10
        correct_answer = int(round((dividend / divisor) * 100))
        if correct_answer >= 1:
            return correct_answer
        else:
            return 0

    def quiz_marking_completed(self):
        self.complete = True
        self.end = now()
        self.save()

    #a wrong question is placed to allow users to answer incorrect questions
    #this would challenge users if the questions are similar
    def add_wrong_question(self, question):
        if len(self.wrong_questions) > 0:
            self.wrong_questions += ','
        if self.completed_attempt:
            self.add_to_score(-1)
        self.save()

    @property
    def get_wrong_questions(self): #returns wrong questions for use in a quiz
        return[int(q) for q in self.wrong_questions.split(',') if q]

    def remove_wrong_questions(self, question):
        current = self.get_wrong_questions
        current.remove(question.id)
        self.wrong_questions = ','.join(map(str, current))
        self.add_to_score(1)
        self.save()

    @property 
    #determines if a user has passed a quiz by scoring over a determined percentage
    def check_if_quiz_is_passed(self):
        return self.get_num_of_questions_right >= self.quiz.quiz_pass_mark 

    @property
    #releases user's quiz result
    def produce_result(self):
        if self.check_if_quiz_is_passed:
            return self.quiz.quiz_pass_notif
        else:
            return self.quiz_fail_notif

    def add_participant_answer(self, question, guess): #adds user answer
        current = json.loads(self.participant_answers)
        current[question.id] = guess
        self.participant_answers = json.dumps(current)
        self.save()

    def get_questions(self, with_answers=False): #collect questions for use in quiz
        question_ids = self._question_ids()
        questions = sorted(self.question_set.filter(id__in=question_ids)
                           .select_subclasses(),
                           key=lambda q: question_ids.index(q.id))
        if with_answers:
            participant_answers = json.loads(self.participant_answers)
            for question in questions:
                question.particpant_answer = participant_answers[str(question.id)]
        return questions

    @property
    def question_with_participant_answers(self):
        return{
            q: q.participant_answer for q in self.get_questions(with_answers=True)
            }
    
    @property
    def get_max_score(self): #determines maximum score in a quiz
        return len(self._question_ids())

    def quizprogression(self):
        answered = len(json.loads(self.participant_answers))
        total = self.get_max_score
        return answered, total
 
class Question(models.Model):
    #model is used to organise questions for use in a quiz
    quiz=models.ManyToManyField(
        Quiz, 
        verbose_name=_("Quiz"), 
        blank=True)
    quiztype=models.ForeignKey(
        QuizType, 
        verbose_name=_("QuizType"),
        blank=True, 
        null=True, on_delete=models.CASCADE)
    figure = models.ImageField(
        upload_to='uploads/%Y/%m/%d',
        blank=True, 
        null=True,
        verbose_name=_("figure"))
    entans=models.CharField(#enter answer 
        max_length=1000,
        default=True,
        blank=False, 
        help_text=_("Enter question"), 
        verbose_name=_('entans'))
    questdescript=models.TextField( #question description
        max_length=2000,
        blank=True, 
        help_text=_("Description of question after being answered"), 
        verbose_name=_('Question Description'))

    objects = InheritanceManager()

    class Meta:
        verbose_name=_("Question")
        ordering=['quiztype']
        
    def __str__(self):
        return self.entans

ANSWER_ORDER_OPTIONS = (
    ('entans', 'entAns'),
    ('none', 'None'),
    )

class MultipleChoice(Question): #intended to organise questions in a multiple choice format 
    answer_order=models.CharField(
        max_length=30,
        null=True,
        blank=True,
        choices=ANSWER_ORDER_OPTIONS,
        help_text=_("the order in which questions are displayed"))

    def check_if_answer_is_correct(self, guess):
        answer=QuizAnswer.objects.get(id=guess)
        if answer.correct is True:
            return True
        else:
            return False

    def order_answers(self, queryset):
        if self.answer_order == 'entans':
            return queryset.order_by('entans')
        if self.answer_order == 'none':
            return queryset.order_by('None')

    def get_answers(self):
        return self.order_answers(QuizAnswer.objects.filter(question=self))

    def get_answers_list(self):
        return[(quizanswer.id, quizanswer.entans) for quizanswer in self.order_answers(QuizAnswer.objects.filter(question=self))]

    def answer_choice_to_string(self, guess):
        return QuizAnswer.objects.get(id=guess).entans

    class Meta:
        verbose_name = "Multiple Choice Question"

class QuizAnswer(models.Model): 
    #model is used to provide answers for the questions so 
    #that users are able to progress                                 
    question = models.ForeignKey(
        MultipleChoice, on_delete=models.CASCADE)
    entans = models.CharField( 
        max_length=1000,
        blank=False,
        help_text=_("enter answer"), 
        verbose_name=_("entAns"))

    correct=models.BooleanField(
        blank=False, 
        default=False, 
        help_text=_("is this a correct answer to the proposed question?"))

    def __str__(self):
        return self.entans


def csv_upload_instance(instance, filename):
    cfui = instance.__class__.objects.filter(user=instance.user) #cfui (csv file upload instance)
    if cfui.exists():
        num_=cfui.last().id + 1
    else:
         num_ = 1
    return u'csv/{num_}/{instance.user.username}/{filename}'

class UploadCSVFormat(models.Model):
    #upload results in a csv data file 
    title = models.CharField(
        max_length=100, 
        blank=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    file = models.FileField(upload_to=csv_upload_instance, 
                            validators=[csv_file_validator_function])
    completed=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

def create_user(data):
    #allows the creation of users
    user = User.objects.create_user(username=data['username'],
                                    password=data['password'],
                                    )
    user.is_admin=False
    user.is_staff=False
    user.save()

def convert_header(csvHeader): 
    header_= csvHeader[0]
    cols = [x.replace('', '_').lower() for x in header_.split(",")]
    return cols

def csv_file_validator_function_post_save(sender, instance, created, *args, **kwargs):
    if not instance.completed:
        csv_file = instance.file
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.reader(io_string, delimiter=';', quotechar='|')
        header_ = next(reader)
        header_cols = convert_header(header_)
        print(header_cols, str(len(header_cols)))
        parsed_items = []

        for line in reader:
            parsed_row_data = {}
            i = 0
            print(line[0].split(','), len(line[0].split(',')))
            row_item = line[0].split(',')
            for item in row_item:
                key = header_cols[i]
                parsed_row_data[key] = item
                i+=1
            create_user(parsed_row_data)
            parsed_items.append(parsed_row_data)
            print(parsed_items)
        csv_file_validator_function.send(sender=instance,
                                         user=instance.user,
                                         csv_file_list=parsed_items)
        instance.completed = True
        instance.save()

post_save.connect(csv_file_validator_function_post_save, sender=UploadCSVFormat)