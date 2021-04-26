from django.shortcuts import render

# Create your views here.
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

#import models
from .models import Student, Exam, Question
from tester import models

import os
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError


def index(request):
    return render(request, 'index.html',{})

class ExamListView(generic.ListView):
    model= Exam

def question_list(request, pk):
    exam = models.Exam.objects.get(id=pk)
    questions = models.Question.objects.all().filter(exam_name=exam)
    context = {
        'exam':exam,
        'questions':questions,
    }
    return render(request, 'tester/question_list.html', context)

class QuestionListView(generic.ListView):
    model=Question

class QuestionDetailView(generic.DetailView):
    model=Question
