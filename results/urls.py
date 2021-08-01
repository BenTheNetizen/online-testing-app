from django.urls import path, re_path
from .views import (
    results,
    render_pdf_view,
)
app_name = 'results'

urlpatterns = [
    path('exam-<pk>/results/', render_pdf_view, name='render-pdf-view'),
    path('', render_pdf_view, name='results'),
]
