from django.contrib import admin
from .models import Exam, SectionInstance, ExamInstance
# Register your models here.

admin.site.register(Exam)
admin.site.register(SectionInstance)
admin.site.register(ExamInstance)
