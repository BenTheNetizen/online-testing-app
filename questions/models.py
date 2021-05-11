from django.db import models
from exams.models import Section
# Create your models here.

class Question(models.Model):
    question_number = models.IntegerField(max_length=1000)
    text = models.CharField(max_length=200)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student_response = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=1000, default="")
    letter = models.CharField(max_length=1000, default="")
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"




    # question = models.TextField(max_length=500)
    # option1 = models.CharField(max_length=100)
    # option2 = models.CharField(max_length=100)
    # option3 = models.CharField(max_length=100)
    # option4 = models.CharField(max_length=100)
    # choose = (('A', 'option1'), ('B', 'option2'), ('C', 'option3'), ('D', 'option4'))
    # correct_answer = models.CharField(max_length=1, choices=choose)
    #
    # class Meta:
    #     ordering = ['id']
    #
    # def check_if_correct(self, guess):
    #     if guess = correct_answer:
    #         return True
    #     else:
    #         return False
    #
    # def get_answers_list(self):
    #     return self.choose
    #
    #
    # def __str__(self):
    #     return str(self.question)
    #
    # def get_absolute_url(self):
    #     return reverse('question-detail', args=[str(self.id)])
