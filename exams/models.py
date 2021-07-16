from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
from django.urls import reverse

class Student(models.Model):
    #user is the username of the student account
    user = models.CharField(primary_key=True, max_length=20, unique=True)

    def __str__(self):
        return str(self.user)

#model for the Exam
class Exam(models.Model):
    name = models.CharField(max_length=100, default=" ")

    class Meta:
        verbose_name_plural = "Exams"
        ordering = ['id']

    def get_sections(self):
        return self.section_set.all()

    def test():
        return str(self.name)

    def __str__(self):
        return str(self.name)

class Section(models.Model):
    name = models.CharField(max_length=100, default=" ")
    #Type = "Reading", "Writing", "Math1", "Math2"
    type = models.CharField(max_length=100, default='none')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    num_questions = models.IntegerField(default=0)
    time = models.IntegerField(default=5, help_text="duration of the section in minutes")
    num_passages = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.name}-{self.exam}"

    def get_questions(self):
        return self.question_set.all()[:self.num_questions]
