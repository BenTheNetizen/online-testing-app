from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('exam', views.ExamListView.as_view(), name='exam'),
    path('take-exam/<int:pk>', views.question_list, name='take-exam'),
    #path('exam/<int:pk>/questions', views.question_list, name='questions'),
    #path('questions', views.QuestionListView.as_view(), name='questions'),
    path('questions/<int:pk>', views.QuestionDetailView.as_view(), name='question-detail'),
]
