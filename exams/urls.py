from django.urls import path
from .views import (
    ExamListView,
    SectionListView,
    exam_view,
    section_view,
    section_data_view,
    save_section_view,
)
app_name = 'exams'

urlpatterns = [
    path('', SectionListView.as_view(), name='main-view'),
    path('<pk>/', section_view, name='section-view'),
    path('<pk>/save/', save_section_view, name='save-section-view'),
    path('<pk>/data/', section_data_view, name='section-data-view')
]
