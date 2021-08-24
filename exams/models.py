from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.dispatch import receiver
# Create your models here.

#model for the Exam
class Exam(models.Model):
    name = models.CharField(max_length=100, default=" ")
    type = models.CharField(max_length=100, default='SAT')

    class Meta:
        verbose_name_plural = "Exams"
        ordering = ['id']

    def get_sections(self):
        return self.section_set.all().order_by('ordering')

    def __str__(self):
        return str(self.name)

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=50, blank=True, null=True)
    parent_email = models.CharField(max_length=100, blank=True, null=True)
    parent_phone_number = models.CharField(max_length=50, blank=True, null=True)
    student_access_code = models.CharField(max_length=50, blank=True, null=True)
    recent_exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

#model for an exam instance
class ExamInstance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    is_extended_time = models.BooleanField(default=False)

class Section(models.Model):
    name = models.CharField(max_length=100, default=" ")
    #Type = "Reading", "Writing", "Math1", "Math2"
    type = models.CharField(max_length=100, default='none')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    num_questions = models.IntegerField(default=0)
    time = models.IntegerField(default=5, help_text="duration of the section in minutes")
    num_passages = models.IntegerField(default=0, blank=True, null=True)
    ordering = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}-{self.exam}"

    def get_questions(self):
        return self.question_set.all()[:self.num_questions]

    def get_section_instance(self):
        return self.sectioninstance_set.all()
#model for a section instance
class SectionInstance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    minutes_left = models.IntegerField(default=0)
    seconds_left = models.IntegerField(default=0)

    def __str__(self):
        return f"User: {self.user}, Exam: {self.exam}, Section: {self.section}, Time Remaining: {self.minutes_left} mins, {self.seconds_left} seconds"
