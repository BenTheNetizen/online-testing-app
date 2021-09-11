from django.urls import path, re_path
from .views import (
    results,
    render_pdf_view,
    render_pdf_of_results,
    render_diagnostic_score_report,
)
app_name = 'results'

urlpatterns = [
    path('exam-<pk>/results/', render_pdf_view, name='render-pdf-view'),
    path('', render_pdf_view, name='results'),
    path('render-pdf-of-results/exam-<pk>', render_pdf_of_results, name='render_pdf_of_results'),
    path('diagnostic-score-report', render_diagnostic_score_report, name='render_diagnostic_score_report'),
]
