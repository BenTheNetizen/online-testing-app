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

"""
<form method="post" encrypt="multipart/form-data">
    {% csrf_token %}
    <label>Upload a file</label>
    <input type="file" name="file">
    <p>Only accepts CSV files</p>
    <button type="submit">Upload</button>
</form>
"""
