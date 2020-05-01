"""
Project Definition of Views
"""
import random
import fnmatch
from django.shortcuts import render
from datetime import datetime
from django.http import HttpRequest
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView
from django.contrib import messages
from django.views.generic.edit import FormView
from django.http import FileResponse, Http404
from .forms import QuestionForm
from .models import Post, Quiz, QuizType, QuizCBM, Attempt, Question, MultipleChoice, QuizAnswer
 
# Create your views here. 

def index(request):
    assert isinstance (request, HttpRequest)
    return render(
        request, 'app/index.html',
        {'title': 'Index Page',
         'year':datetime.now().year,
         })
def auth_view(request):
    if not request.user.is_authenticated:
        return redirect('app/loginpage.html' % (settings.LOGIN_URL, request.path))

def userhome(request):
    assert isinstance (request, HttpRequest)
    return render(
        request, 'app/userhome.html',
        {'title': 'User Home',
         'message': 'welcome', 
         'year': datetime.now().year,
         })
def about_project(request):
    assert isinstance (request, HttpRequest)
    return render(
        request, 'app/aboutproject.html',
        {'title': 'About Project',
         'message': 'welcome', 
         'year': datetime.now().year,
         })
def articleview(request):
    assert isinstance (request, HttpRequest)
    return render(
        request, 'app/article.html',
        {'title': 'Article',
         'message': 'welcome', 
         'year': datetime.now().year,
         })
def profilepage(request):
    assert isinstance (request, HttpRequest)
    return render(
        request, 'app/accounts/profilepage.html',
        {'title': 'User Home',
         'message': 'welcome', 
         'year': datetime.now().year,
         })
def siteblog(request):
    assert isinstance (request, HttpRequest)
    return render(
        request, 'app/blog/siteblog.html', 
        {'title': 'Blog', 
         'year':datetime.now().year,
         })
def maliciousextensionspage(request):
    assert isinstance (request, HttpRequest)
    return render(
        request, 'app/maliciousextensions.html',
        {'title': 'Malicious Extensions',
         'message': 'welcome', 
         'year': datetime.now().year,
         })
def post_list(request):
    posts=Post.objects.filter(
        published_date__Ite=timezone.now()).order_by('published_date')
    (request, 'app/siteblog.html', {'posts': posts})

def whatismalwarevideo(request):
    assert isinstance (request, HttpRequest)
    return render(
        request, 'app/video/whatismalwarevideo.html',
        {'title': 'What is Malware', 
          'year':datetime.now().year,  
            })

def aptvideo(request):
     assert isinstance (request, HttpRequest)
     return render(
        request, 'app/video/aptvideo.html',
        {'title': 'Advanced Persistent Threat Video', 
          'year':datetime.now().year,  
            })

def scamsvideo(request):
     assert isinstance (request, HttpRequest)
     return render(
        request, 'app/video/scamsvideo.html',
        {'title': 'Scams Video', 
          'year':datetime.now().year,  
            })

def hackersvideo(request):
     assert isinstance (request, HttpRequest)
     return render(
        request, 'app/video/hackersvideo.html',
        {'title': 'Hackers Video', 
          'year':datetime.now().year,  
            })

def iotvideo(request):
     assert isinstance (request, HttpRequest)
     return render(
        request, 'app/video/iotvideo.html',
        {'title': 'Internet of Things Video', 
          'year':datetime.now().year,  
            })

def quiz_page_menu_view(request):
    assert isinstance (request, HttpRequest)
    return render(
        request, 'app/quiz_page_menu.html',
        {'title': 'Quiz Page Menu',
         'message': 'welcome', 
         'year': datetime.now().year,
         })


#*********************ADMIN QUIZ VIEW SECTION***************************
class QuizMarkingMixin(object):    #QuizMarkerMixin
    @method_decorator(login_required)
    @method_decorator(permission_required('quiz.view_attempts'))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkingMixin, self).dispatch(*args, **kwargs)

class QuizAttemptFilterTitleMixin(object):#SittingFilterTitleMixin
    def get_queryset(self):
        queryset=super(QuizAttemptFilterTitleMixin, self),get_queryset()
        attempt_filter=self.request.GET.get('attempt_filter')
        if attempt_filter:
            queryset=queryset.filter(quiz__title__icontains=attempt_filter)

        return queryset 

class QuizListView(ListView):
    model = Quiz
    template_name ='app/adminquiz/onlinequizfunctions/quizlist.html'
    def get_queryset(self):
      queryset = super(QuizListView, self).get_queryset()
      
      return queryset.filter(quiz_outline=False)

class QuizInfoView(DetailView): #QuizDetailView
    model = Quiz
    slug_field = 'url'
    def get(self, request, *args, **kwargs):

        self.object = self.get_object()
        if self.object.quiz_outline and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        context=self.get_context_data(object = self.object)
        return self.render_to_response(context)


class QuizTypeListView(ListView): #CategoriesListView
    model = QuizType

class ListQuizByQuizTypeView(ListView): #ViewQuizListByCategory
    model = Quiz
    template_name='display_quiz_type.html'

    def dispatch(self, request, *args, **kwargs):
       self.quiztype = get_object_or_404(
          QuizType, quiztype=self.kwargs['quiztype_name'])

       return super(ListQuizByQuizTypeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ListQuizByQuizTypeView, self).get_context_data(**kwargs)
        
        context['quiztype'] = self.quiztype
        return context

    def get_queryset(self):
        queryset=super(ListQuizByQuizTypeView, self).get_queryset()
        return queryset.filter(quiztype, quiz_outline=False)

class QuizMarkingQueue(QuizMarkingMixin, QuizAttemptFilterTitleMixin, ListView): #QuizMarkingList
    model = Attempt 
    def get_queryset(self):
        queryset=super(QuizMarkingQueue, self).get_queryset().filter(complete=True)
        user_filter=self.request.GET.get('user_filter')
        if user_filter:
            queryset=queryset.filter(user__username__icontains=user_filter)
        return queryset

    class Meta:
          pass

class QuizScoringFeature(QuizMarkingMixin, DetailView): #QuizMarkingDetail
    model = Attempt

    def post(self, request, *args, **kwargs):
        attempt = self.get_object()
        q_configure = request.POST.get('qid', None)
        if q_configure:
            q = Question.objects.get_subclass(id=int(q_configure))
            if int(q_configure) in attempt.get_wrong_questions:
                attempt.remove_wrong_question(q)
            else:
                attempt.add_wrong_question(q)
        return self.get(request)
    
    def get_context_data(self, **kwargs):
        context = super(QuizScoringFeature, self).get_context_data(**kwargs)
        context['questions'] = context['attempt'].get_questions(with_answers=True)
        return context

class UserProgressView(TemplateView):
    template_name='app/adminquiz/quizcbm.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
     return super(UserProgressView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
     context = super(UserProgressView, self).get_context_data(**kwargs)
     quizcbm, c = QuizCBM.objects.get_or_create(user=self.request.user)
     context['qtype_result'] = quizcbm.display_attempts()
     
     return context

class TakeQuiz(FormView):
    form_class = QuestionForm
    template_name = 'question.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['quiz_name'])
        if self.quiz.quiz_outline and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        self.logged_in_user = self.request.user.is_authenticated

        if self.logged_in_user:
             self.attempt = Attempt.objects.user_attempt(request.user, self.quiz)
        
        if self.attempt is False:
            return render(request, 'first_attempt_comp.html')
        return super(TakeQuiz, self).dispatch(request, *args, **kwargs)

    def get_form(self, form_class=QuestionForm):
        if self.logged_in_user:
            self.question = self.attempt.get_first_question()
            self.quizcbm = self.attempt.quizprogression()
        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(TakeQuiz, self).get_form_kwargs()
        return dict(kwargs, question=self.question)
    
    def form_valid(self, form):
        if self.logged_in_user:
            self.form_valid_user(form)
            if self.attempt.get_first_question() is False:
                return self.final_result_user()
        self.request.POST = {}
        return super(TakeQuiz, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(TakeQuiz, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz 
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
            if hasattr(self, 'quizcbm'):
                context['quizcbm'] = self.quizcbm
            return context

    def valid_form_user(self, form):
        quizcbm, c = QuizCBM.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data['quizanswers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.attempt.add_to_score(1)
            quizcbm.update_score(self.question, 1, 1)
        else:
            self.attempt.add_wrong_question(self.question)
            quizcbm.update_score(self.question, 0, 1)

        if self.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_answer': self.question,
                             'answers': self.question.get_questions(),
                             'question_type': {self.question.__class__.__name__: True}}
        else:
            self.previous = {}

        self.attempt.add_participant_answer(self.question, guess)
        self.attempt.remove_first_question()

    def final_result_user(self):
        results = {'quiz': self.quiz, 
                   'score': self.attempt.get_present_score,
                   'max_score': self.attempt.get_max_score,
                   'percentage': self.attempt.get_score_percentage,
                   'attempt': self.attempt,
                   'previous': self.previous,
                   }
        self.attempt.quiz_marking_completed()

        if self.quiz.answers_at_end:
            results['questions'] = \
                self.sitting.get_questions(with_answers = True)
            results['Wrong Questions'] = \
                self.attempt.get_wrong_questions

        return render(self.request, 'result.html', results)

    def take_quiz(request):
      return render(request, 'quiz_menu.html', {})

#************************QUIZ TEMPLATE VIEWS******************************
def quiztype_list_view(request):
     assert isinstance (request, HttpRequest)
     return render(
        request, 'app/adminquiz/onlinequizfunctions/quiztype_list.html',
        {'title': 'QuizType List View', 
          'year':datetime.now().year,  
            })

def quiz_info_url_view(request):
     assert isinstance (request, HttpRequest)
     return render(
        request, 'app/adminquiz/onlinequizfunctions/quizdetail.html',
        {'title': 'Quiz Info View', 
          'year':datetime.now().year,  
            })

def take_quiz_view(request):
     assert isinstance (request, HttpRequest)
     return render(
        request, 'app/adminquiz/question.html',
        {'title': 'Take Quiz View', 
          'year':datetime.now().year,  
            })

def list_quiz_by_type_view(request):
     assert isinstance (request, HttpRequest)
     return render(
        request, 'app/adminquiz/display_quiz_type.html',
        {'title': 'Display Quiz Type', 
          'year':datetime.now().year,  
            })

def quiz_menu_list_view(request):
     assert isinstance (request, HttpRequest)
     return render(
        request, 'app/adminquiz/onlinequizfunctions/quizlist.html',
        {'title': 'Quiz List', 
          'year':datetime.now().year,  
            })

def quiz_marking_detail_type_view(request):
     assert isinstance (request, HttpRequest)
     return render(
        request, 'app/adminquiz/display_quiz_type.html',
        {'title': 'Display Quiz Type', 
          'year':datetime.now().year,  
            })

def user_cbm_view(request):
     assert isinstance (request, HttpRequest)
     return render(
        request, 'app/adminquiz/quizcbm.html',
        {'title': 'Display Quiz Progress', 
          'year':datetime.now().year,  
            })
