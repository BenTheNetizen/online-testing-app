from django.contrib import admin
from .models import Question, Answer, Result, Section, Student_Answer
# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(Section)
admin.site.register(Student_Answer)
