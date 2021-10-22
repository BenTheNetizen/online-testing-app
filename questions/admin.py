from django.contrib import admin
from .models import Question, Answer, Result, Section, Student_Answer
# Register your models here.

class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_filter = ("exam", "section__type")

class QuestionInline(admin.TabularInline):
    model = Question

class SectionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(Section, SectionAdmin)
admin.site.register(Student_Answer)
