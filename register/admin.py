from django.contrib import admin
from exams.models import Student
from .models import StudentAccessCode
# Register your models here.

admin.site.register(Student)
admin.site.register(StudentAccessCode)
