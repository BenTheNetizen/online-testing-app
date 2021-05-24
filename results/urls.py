from django.urls import path, re_path
from .views import (
    results,
)
app_name = 'results'

urlpatterns = [
    path('exam-<pk>/results/', results),
    path('', results, name='results'),
]
