from django.urls import path, re_path
from django.urls import include
from .views import (
    index,
    exam_list_view,
    exam_list_recent_exam_view,
    exam_list_data_view,
    exam_list_reset_view,
    exam_list_change_time_view,
    problem_database_view,
    problem_database_data_view,
    section_reset_view,
    start_exam_view,
    section_directions_view,
    section_view,
    section_review_view,
    section_math_data_view,
    section_passage_data_view,
    save_timer_view,
    save_section_view,
    save_question_view,
    get_next_section_view,
    section_break_view,
    file_upload,
)
app_name = 'exams'


urlpatterns = [
    path('', index, name='index'),
    path('problem-database/', problem_database_view, name='problem-database-view'),
    path('problem-database/data', problem_database_data_view, name='problem-database-data-view'),
    path('exam-list/', exam_list_view, name="exam-list-view"),
    path('exam-list/recent-exam', exam_list_recent_exam_view, name="exam-list-recent-exam-view"),
    path('exam-list/exam-<pk>/data', exam_list_data_view, name="exam-list-data-view"),
    path('exam-list/exam-<pk>/reset', exam_list_reset_view, name="exam-list-reset-view"),
    path('exam-list/exam-<pk>/change-time', exam_list_change_time_view, name="exam-list-change-time-view"),
    path('exam-list/exam-<pk>/<str:section_name>/reset', section_reset_view, name="section-reset-view"),
    path('exam-<pk>/start-exam/', start_exam_view, name="start-exam-view"),
    path('exam-<pk>/<str:section_name>/section-directions/', section_directions_view, name="section-directions-view"),
    #this redirects to the 'results' app
    path('exam-<pk>/results/', include('results.urls', namespace='results')),
    #this url begins the exam
    path('exam-<pk>/<str:section_name>/', section_view, name='section-view'),
    path('exam-<pk>/<str:section_name>/review/', section_review_view, name='section-review-view'),
    re_path(r'^exam-(?P<pk>[0-9]+)/(?P<section_name>[a-z0-9]+)/save$', save_section_view, name='save-section-view'),
    re_path(r'^exam-(?P<pk>[0-9]+)/(?P<section_name>[a-z0-9]+)/save-timer$', save_timer_view, name='save-timer-view'),
    re_path(r'^exam-(?P<pk>[0-9]+)/(?P<section_name>[a-z0-9]+)/(review/)?data$', section_math_data_view, name='section-math-data-view'),
    re_path(r'^exam-(?P<pk>[0-9]+)/(?P<section_name>[a-z0-9]+)/(review/)?passage-(?P<passage_num>[0-9]+)/data$', section_passage_data_view, name='section-passage-data-view'),
    re_path(r'^exam-(?P<pk>[0-9]+)/(?P<section_name>[a-z0-9]+)/save-question$', save_question_view, name='save-question-view'),
    re_path(r'^exam-(?P<pk>[0-9]+)/(?P<section_name>[a-z0-9]+)/get-next-section$', get_next_section_view, name='get-next-section-view'),
    path('exam-<pk>/break<int:break_num>/<str:next_section_name>/', section_break_view, name='section-break-view'),
    path('upload-csv/', file_upload, name="file-upload"),

]
