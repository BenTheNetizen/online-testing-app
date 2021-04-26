from django.contrib import admin

# Register your models here.
from .models import Student, Exam, Question

admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(Question)
