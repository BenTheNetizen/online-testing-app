from django.urls import path, re_path
from django.urls import include
from .views import (
    index,
    ExamListView,
    #exam_view,
    section_view,
    section_data_view,
    save_section_view,
    section_break_view,
    file_upload,
    test,
)
app_name = 'exams'


urlpatterns = [
    path('', index, name='index'),
    path('exam-list/', ExamListView.as_view(), name="exam-list-view"),
    #this redirects to the 'results' app
    path('exam-<pk>/results/', include('results.urls', namespace='results')),
    #this url begins the exam
    path('exam-<pk>/<str:section_name>/', section_view, name='section-view'),
    re_path(r'^exam-(?P<pk>[0-9]+)/(?P<section_name>[a-z0-9]+)/save$', save_section_view, name='save-section-view'),
    re_path(r'^exam-(?P<pk>[0-9]+)/(?P<section_name>[a-z0-9]+)/data$', section_data_view, name='section-data-view'),
    path('exam-<pk>/break<int:break_num>', section_break_view, name='section-break-view'),
    path('upload-csv/', file_upload, name="file-upload"),

]
