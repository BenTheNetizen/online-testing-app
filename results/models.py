from django.db import models
from exams.models import Section
from django.contrib.auth.models import User
# Create your models here.

"""
class Result(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.FloatField()

    def __str__(self):
        return str(self.pk)
"""
