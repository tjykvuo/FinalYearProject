"""projectsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url
from django.urls import include, path, re_path
from datetime import datetime
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from app.views import QuizTypeListView, TakeQuiz, ListQuizByQuizTypeView,\
   QuizMarkingQueue, QuizScoringFeature, UserProgressView, QuizInfoView, QuizListView

urlpatterns = [
    #MAIN SITE NAVIGATION
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('siteblog/', views.siteblog, name='siteblog'),
    path('aboutproject/', views.about_project, name='aboutproject'),
    path('userhome/', views.userhome, name='userhome'),
    path('profilepage/', views.profilepage, name='profilepage'),
    path('quiztypelistpage/', views.quiztype_list_view, name='quiztype_list_url'),
    path('iotvideo/', views.iotvideo, name = 'iotvideo'),
    path('article/', views.articleview, name = 'articleurl'),
    path('maliciousextensions/', views.maliciousextensionspage, name ='maliciousextensionspath'),

    #PROJECT VIDEOS
    path('whatismalwarevideo/', views.whatismalwarevideo, name= 'whatismalwarevideo'),
    path('aptvideo/', views.aptvideo, name = 'aptvideo'),
    path('scamsvideo/', views.scamsvideo, name = 'scamsvideo'),
    path('hackersvideo/', views.hackersvideo, name = 'hackersvideo'),
    path('iotvideo/', views.iotvideo, name = 'iotvideo'),


    #URL PATHS
    path('usercbm/', views.user_cbm_view, name = 'usercbm'),
    
    #AUTHENTICATION
    path('login/',
         LoginView.as_view
         (
             template_name='app/loginpage.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),


    #REGULAR EXPRESSION PATHS
    re_path(r'^quizzes/$', view = QuizListView.as_view(), name = 'quiz_index'),
    re_path(r'^quiztype/$', view = QuizTypeListView.as_view(), name='quiz_type_list'),
    re_path(r'^listquizbyquiztypeview/$', view = ListQuizByQuizTypeView.as_view(), name='list_quiz_type_view'),
    re_path(r'^marking/$', view = QuizMarkingQueue.as_view(), name = 'quiz_marking'),
    re_path(r'^marking/(?P<pk>[\d.]+)/$', view=QuizScoringFeature.as_view(),name='quiz_marking_detail'),
    re_path(r'^(?P<slug>[\w-]+)/$', view=QuizInfoView.as_view(), name='quiz_start'),
    re_path(r'^(?P<quiz_name>[\w-]+)/take/$', view=TakeQuiz.as_view(), name='take_quiz'),
    re_path(r'^progress/$', view=UserProgressView.as_view(), name='user_progress_view'),
]

