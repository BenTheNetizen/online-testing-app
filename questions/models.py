from django.db import models
from exams.models import Section, User, Exam
# Create your models here.

class Question(models.Model):
    question_number = models.IntegerField(default=-1)
    text = models.CharField(max_length=1000, default=" ")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    material = models.ImageField(null=True, blank=True)
    passage = models.IntegerField(null=True, blank=True)
    correct_answer = models.CharField(max_length=100, default="")
    categories = models.CharField(max_length=100, null=True, blank=True)

    
    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=500, default="", null=True, blank=True)
    letter = models.CharField(max_length=1, default="")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question: {self.question.text}, Answer: {self.text}"

class Result(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    time_finished = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"User: {self.user}, Exam: {self.exam.name}, Section: {self.section.type}, Raw Score: {self.score}"

class Student_Answer(models.Model):
    answer = models.CharField(max_length=100, default="")
    question_number = models.IntegerField(default=0)
    section = models.CharField(max_length=30, default="")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"User: {self.user}, Exam: {self.exam}, Section: {self.section}, Question: {self.question_number}, Answer: {self.answer}"
