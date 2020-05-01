import re
from django.urls import include, path, re_path
from django.conf.urls import url
from django.urls import path
from datetime import datetime
from django.contrib.auth.views import LoginView, LogoutView
from app.views import QuizMarkingView, QuizAttemptFilter, QuizTypeListView, ListQuizByQuizTypeView, QuizMarkingQueue, QuizScoringFeature, TakeQuiz, UserProgressView, QuizInfoView, Post
from app import forms, views

urlpatterns = [
    #admin post urls
    path('login/', views.LoginView.as_view(), name='login'),
	path('siteblog/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),

    #path('quizlistv/', views.QuizListView.as_view(), name = 'Quiz_List'),
    #path('quiztypelist/', views.QuizTypeListView.as_view(), name = 'Quiz_Type_List'),
    #path('quizinfo/', views.QuizInfoView.as_view(), name = 'Quiz_Info_V'),
    #path('takequiz/', views.TakeQuiz.as_view(), name = 'Take_Quiz'),
    #path('listquizbytype/', views.ListQuizByQuizTypeView.as_view(), name = 'List_Quiz_By_Type'),
    #path('quizmarkinglist/', views.QuizMarkingQueue.as_view(), name = 'Quiz_Marking_Q'),
    #path('quizmarkingdetail/', views.QuizScoringFeature.as_view(), name = 'Quiz_Score_F'),
    #path('userprogress/', views.UserProgressView.as_view(), name = 'User_Progress_View'),

    #admin quiz urls  
    #re_path(r'^quiztype/$', view = QuizTypeListView.as_view(), name='quiz_type_list'),
    #re_path(r'^listquizbyquiztypeview/$', view = ListQuizByQuizTypeView.as_view(), name='list_quiz_type_view'),
    #re_path(r'^marking/$', view = QuizMarkingQueue.as_view(), name = 'quiz_marking'),
    #re_path(r'^marking/(?P<pk>[\d.]+)/$', view=QuizScoringFeature.as_view(),name='quiz_marking_detail'),
    #re_path(r'^(?P<slug>[\w-]+)/$', view=QuizInfoView.as_view(), name='quiz_start_page'),
    #re_path(r'^(?P<quiz_name>[\w-]+)/take/$', view=TakeQuiz.as_view(), name='take_quiz'),
    #re_path(r'^progress/$', view=UserProgressView.as_view(), name='user_progress_view'),
    
    #____________________________________________________________
    #|QuizTypeListView:      | lists all quizzes                |
    #|ListQuizByQuizTypeView:| lists all quizzes by type        |
    #|QuizMarkingQueue:      | handles quiz marking             |
    #|QuizScoringFeature:    | handles marking                  |
    #|TakeQuiz:              | quiz question                    |
    #|UserProgressView:      | handles user progress            |
    #|QuizInfoView:          | traverses user to TakeQuiz View  |                           
    #|__________________________________________________________|
    ]