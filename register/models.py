from django.db import models

# Create your models here.

class StudentAccessCode(models.Model):
    code = models.CharField(max_length=100, default=" ")
    class Meta:
        verbose_name_plural = "Student Access Codes"
        ordering = ['id']
    
    def __str__(self):
        return self.code