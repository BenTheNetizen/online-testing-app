from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
from django.urls import reverse


class Student(models.Model):
    #user is the username of the student account
    user = models.CharField(primary_key=True, max_length=20, unique=True)

    #name is the name of the student
    name = models.CharField(max_length=30)

    password = models.CharField(max_length=24)

    slug = models.SlugField(max_length=200)

    def __str__(self):
        return str(self.user)

#model for the Exam
class Exam(models.Model):
    exam_name = models.CharField(max_length=50)
    num_questions = models.IntegerField(default=0)


    def __str__(self):
        return str(self.exam_name)




class Question(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    exam_name = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.TextField(max_length=500)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    choose = (('A', 'option1'), ('B', 'option2'), ('C', 'option3'), ('D', 'option4'))
    answer = models.CharField(max_length=1, choices=choose)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return str(self.question)

    def get_absolute_url(self):
        return reverse('question-detail', args=[str(self.id)])
