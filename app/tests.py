"""
This file makes use of the unittest module to perform testing when 'manage.py test' is run 
"""
from importlib import import_module
from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.http import HttpRequest
from django.test import Template, Context 
from django.test import TestCase
from django.utils.six import StringIO
from django.utils.translation import ugettext_lazy as _
from .models import Post, Quiz, QuizType, QuizCBM, Attempt,\
   Question, MultipleChoice, QuizAnswer

# Create your tests here.

# TODO: Configure your database in settings.py and sync before running tests.

class ViewTest(TestCase):
    """Tests written for the application views"""
    if django.VERSION[:2] >= (1, 7):
        """Django 1.7 requires a setup() in order to run tests in PTVS(Python Tools for Visual Studio)"""
        @classmethod
        def setUpClass(cls):
            super(ViewTest, cls).setUpClass()
            django.setup()

    def test_index(self):
        """Runs a test of the landing page"""
        response=self.client.get('')
        self.assertContains(response, 'Index Page', 1, 200)

    def test_userhome(self):
        """Runs a test of the user home page"""
        response=self.client.get('/userhome')
        self.assertContains(response, 'Home Page', 3, 200)

    def test_siteblog(self):
        """Runs a test of the site blog page"""
        response=self.client.get('/siteblog')
        self.assertContains(response, 'Site Blog', 3, 200)

    def test_profilepage(self):
        """Runs a test of the profile page"""
        response=self.client.get('/profilepage')
        self.assertContains(response, 'Profilepage', 3, 200)

    def test_malwarevideo(self):
        """Runs a test of the malware video page"""
        response=self.client.get('/whatismalwarevideo')
        self.assertContains(response, 'Malware Video', 3, 200)

    def test_aptvideo(self):
        """Runs a test of the apt video page"""
        response=self.client.get('/aptvideo')
        self.assertContains(response, 'APT Video', 3, 200)
    
    def test_hackervideo(self):
        """Runs a test of the hacker video page"""
        response=self.client.get('/hackersvideo')
        self.assertContains(response, 'Hacker Video', 3, 200)

    def test_iotvideo(self):
        """Runs a test of the iot video page"""
        response=self.client.get('/iotvideo')
        self.assertContains(response, 'IoT Video', 3, 200)

    def test_scamvideo(self):
        """Runs a test of the scams video page"""
        response=self.client.get('/scamsvideo')
        self.assertContains(response, 'Scams Video', 3, 200)

#*****************************QUIZ TESTS******************************************
class TestQuizType(TestCase):
    def setUp(self):
        self.qt1 = QuizType.objects.new_quiz_type(quiztype='blueberries')
    
    def test_quiztypes(self):
        self.assertEqual(self.qt1.quiztype, 'blueberries')

class TestQuiz(TestCase):
    def setUp(self):
        self.qt1=QuizType.objects.new_quiz_type(quiztype='berries')
        self.quiz1 = Quiz.objects.create(id=1,
                                         title='test quiz 1',
                                         descriptor='d1',
                                         url='tq1')
        self.quiz2 = Quiz.objects.create(id=2,

                                         title='test quiz 2',

                                         descriptor='d2',

                                         url='t q2')

        self.quiz3 = Quiz.objects.create(id=3,

                                         title='test quiz 3',

                                         descriptor='d3',

                                         url='t   q3')

        self.quiz4 = Quiz.objects.create(id=4,

                                         title='test quiz 4',

                                         descriptor='d4',

                                         url='T-!£$%^&*Q4')



        self.question1 = MultipleChoice.objects.create(id=1,

                                                   content='squawk')

        self.question1.quiz.add(self.quiz1)

    def test_quiz_url(self):
        self.assertEqual(self.quiz1.url, 'tq1')
        self.assertEqual(self.quiz2.url, 't-q2')
        self.assertEqual(self.quiz3.url, 't-q3')
        self.assertEqual(self.quiz4.url, 't-q4')

    def test_quiz_options(self):
        q5 = Quiz.objects.create(id=5, 
                                 title='test quiz 5',
                                 descriptor='d5',
                                 url='tq5',
                                 quiztype='self.qt1',
                                 attempt_record=True)

        self.assertEqual(q5.quiztype.quiztype, self.qt1.quiztype)

        self.assertEqual(q5.variable_order, False)

        self.assertEqual(q5.answers_at_end, False)

        self.assertEqual(q5.attempt_record, True)

    def test_quiz_one_quiz_effort(self):
        self.quiz1.one_quiz_effort = True
        self.quiz1.save()
        
        self.assertEqual(self.quiz1.attempt_record, True)

    def test_show_max_mark(self):
        self.assertEqual(self.quiz1.get_max_score, 1)
    
    def test_get_questions(self):
        self.assertIn(self.question1, self.quiz1.get_questions())

    def test_score_id(self):
        self.assertEqual(self.quiz1.score_id(), '1_score')

    def test_anon_quiz_list(self):
        self.assertEqual(self.quiz1.anon_quiz_list(), '1_q_list')

    def test_quiz_pass_mark(self):
        self.assertEqual(self.quiz1.quiz_pass_mark, False)
        self.quiz1.quiz_pass_mark = 50
        self.assertEqual(self.quiz1.quiz_pass_mark, 50)
        self.quiz1.quiz_pass_mark = 10
        with self.assertRaises(ValidatorError):
            self.quiz1.save()

class TestQuizCBM(TestCase):
    def setUp(self):
        self.qt1 = QuizType.objects.new_quiz_type(quiztype='berries')

        self.quiz1 = Quiz.objects.create(id= 1,
                                         title='test quiz 1',
                                         descriptor='d1',
                                         url ='tq1')
        self.quiz2 = Quiz.objects.create(id=2,
                                         title='test quiz 2',
                                         descriptor='d2',
                                         url='t q2')
        self.quiz3 = Quiz.objects.create(id=3,
                                         title='test quiz 3',
                                         descriptor='d3',
                                         url='t   q3')
        self.quiz4 = Quiz.objects.create(id=4,
                                         title='test quiz 4',
                                         descriptor='d4',
                                         url='T-!£$%^&*Q4')

        self.question1 = MCQuestion.objects.create(id=1,
                                                   content='squawk')
        self.question1.quiz.add(self.quiz1)

    def test_quiz_url(self):
        self.assertEqual(self.quiz1.url, 'tq1')
        self.assertEqual(self.quiz2.url, 't-q2')
        self.assertEqual(self.quiz3.url, 't-q3')
        self.assertEqual(self.quiz4.url, 't-q4')

    def test_quiz_options(self):
        q5 = Quiz.objects.create(id=5,
                                 title='test quiz 5',
                                 descriptor='d5',
                                 url='tq5',
                                 quiztype=self.qt1,
                                 attempt_record= True)

        self.assertEqual(q5.quiztype.quiztype, self.qt1.quiztype)
        self.assertEqual(q5.variable_order, False)
        self.assertEqual(q5.answers_at_end, False)
        self.assertEqual(q5.attempt_record, True)

    def test_quiz_one_quiz_effort(self):
        self.quiz1.one_quiz_effort = True
        self.quiz1.save()

        self.assertEqual(self.quiz1.attempt_record, True)

    def test_get_max_score(self):
        self.assertEqual(self.quiz1.get_max_score, 1)

    def test_get_questions(self):
        self.assertIn(self.question1, self.quiz1.get_questions())

    def test_score_id(self):
        self.assertEqual(self.quiz1.score_id(), '1_score')

    def test_anon_quiz_list(self):
        self.assertEqual(self.quiz1.anon_quiz_list(), '1_q_list')

    def test_quiz_pass_mark(self):
        self.assertEqual(self.quiz1.quiz_pass_mark, False)
        self.quiz1.quiz_pass_mark = 5
        self.assertEqual(self.quiz1.quiz_pass_mark, 5)
        self.quiz1.quiz_pass_mark = 101
        with self.assertRaises(ValidationError):
            self.quiz1.save()

class TestQuizCBM(TestCase):
    def setUp(self):
        self.qt1 = QuizType.objects.new_quiz_type(quiztype='berries')

        self.quiz1 = Quiz.objects.create(id= 1,
                                         title='test quiz 1',
                                         descriptor='d1',
                                         url ='tq1')
        self.question1 = MultipleChoice.objects.create(content='squawk',
                                                       quiztype=self.qt1)
        self.user = User.objects.create_user(username='defuser',
                                             password='def_user')
        self.cbm1 = QuizCBM.objects.new_progress(self.user)

    def test_list_all_emp(self):
        self.assertEqual(self.cbm1.score, '')

        quiztype_dict = self.cbm1.displayQuizTypeScores
        self.assertIn(str(list(quiztype_dict.keys())[0]), self.cbm1.result)
        self.assertIn(self.qt1.quiztype, self.cbm1.result)
#*******************CONTINUE CLASS UNTIL TEST SITTING*************************** 

class TestSitting(TestCase):
    def setUp(self):
        self.quiz1 = Quiz.objects.create(id=1,
                                         title='test quiz 1',
                                         description='d1',
                                         url='tq1',
                                         pass_mark=50,
                                         success_text="Well done",
                                         fail_text="Bad luck")

        self.question1 = MultipleChoice.objects.create(id=1,
                                                   entans='squawk')
        self.question1.quiz.add(self.quiz1)

        self.answer1 = QuizAnswer.objects.create(id=123,
                                             question=self.question1,
                                             entans='bing',
                                             correct=False)

        self.question2 = MultipleChoice.objects.create(id=2,
                                                   entans='squeek')
        self.question2.quiz.add(self.quiz1)

        self.answer2 = QuizAnswer.objects.create(id=456,
                                             question=self.question2,
                                             entans='bong',
                                             correct=True)

        self.user = User.objects.create_user(username='user_name',
                                             password='pass_word')

        self.attempt = Attempt.objects.new_attempt(self.user, self.quiz1)

    def test_get_next_remove_first(self):
        self.assertEqual(self.attempt.get_first_question(),
                         self.question1)

        self.attempt.remove_first_question()
        self.assertEqual(self.attempt.get_first_question(),
                         self.question2)

        self.attempt.remove_first_question()
        self.assertEqual(self.attempt.get_first_question(), False)

        self.attempt.remove_first_question()
        self.assertEqual(self.attempt.get_first_question(), False)

    def test_scoring(self):
        self.assertEqual(self.attempt.get_present_score, 0)
        self.assertEqual(self.attempt.check_if_quiz_is_passed, False)
        self.assertEqual(self.attempt.result_message, 'Bad luck')

        self.attempt.add_to_score(1)
        self.assertEqual(self.attempt.get_present_score, 1)
        self.assertEqual(self.attempt.get_score_percentage, 50)

        self.attempt.add_to_score(1)
        self.assertEqual(self.attempt.get_present_score, 2)
        self.assertEqual(self.attempt.get_score_percentage, 100)

        self.attempt.add_to_score(1)
        self.assertEqual(self.attempt.get_present_score, 3)
        self.assertEqual(self.attempt.get_score_percentage, 100)

        self.assertEqual(self.attempt.check_if_quiz_is_passed, True)
        self.assertEqual(self.attempt.result_message, 'Well done')

    def test_incorrect_and_complete(self):
        self.assertEqual(self.attempt.get_wrong_questions, [])

        self.attempt.add_wrong_question(self.question1)
        self.assertIn(1, self.attempt.get_wrong_questions)

        self.attempt.add_wrong_question(question3)
        self.assertIn(3, self.attempt.get_incorrect_questions)

        self.assertEqual(self.attempt.completed_attempt, False)
        self.attempt.mark_quiz_complete()
        self.assertEqual(self.attempt.completed_attempt, True)

        self.assertEqual(self.sitting.current_score, 0)
        self.attempt.add_wrong_question(self.question2)
        self.assertEqual(self.attempt.present_score, -1)

    def test_add_participant_answer(self):
        guess = '123'
        self.attempt.add_participant_answer(self.question1, guess)

        self.assertIn('123', self.attempt.participant_answer)

    def test_return_questions_with_answers(self):
        '''
        Also tests attempt.get_questions(with_answers=True)
        '''
        self.attempt.add_participant_answer(self.question1, '123')
        self.attempt.add_participant_answer(self.question2, '456')

        participant_answers = self.attempt.questions_with_participant_answers
        self.assertEqual('123', participant_answers[self.question1])
        self.assertEqual('456', participant_answers[self.question2])

    def test_remove_wrong_answer(self):
        self.attempt.add_wrong_question(self.question1)
        self.attempt.add_wrong_question(self.question2)
        self.attempt.remove_wrong_question(self.question1)
        self.assertEqual(self.attempt.wrong_questions, '2')
        self.assertEqual(self.attempt.present_score, 1)

    def test_return_user_sitting(self):
        via_manager = Attempt.objects.user_attempt(self.user, self.quiz1)
        self.assertEqual(self.attempt, via_manager)

    def test_progress_tracker(self):
        self.assertEqual(self.attempt.quizprogression(), (0, 2))
        self.attempt.add_participant_answer(self.question1, '123')
        self.assertEqual(self.attempt.quizprogression(), (1, 2))
#**********************CONTINUE FROM THIS POINT******************************