from django.db import models
from exams.models import Section, User, Exam
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
# Create your models here.

""" Whenever ANY model is deleted, if it has a file field on it, delete the associated file too"""
@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            instance_file_field = getattr(instance,field.name)
            delete_file_if_unused(sender,instance,field,instance_file_field)

""" Delete the file if something else get uploaded in its place"""
@receiver(pre_save)
def delete_files_when_file_changed(sender,instance, **kwargs):
    # Don't run on initial save
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field,models.FileField):
            #its got a file field. Let's see if it changed
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                # We are probably in a transaction and the PK is just temporary
                # Don't worry about deleting attachments if they aren't actually saved yet.
                return
            instance_in_db_file_field = getattr(instance_in_db,field.name)
            instance_file_field = getattr(instance,field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender,instance,field,instance_in_db_file_field)

""" Only delete the file if no other instances of that model are using it"""
def delete_file_if_unused(model,instance,field,instance_file_field):
    dynamic_field = {}
    dynamic_field[field.name] = instance_file_field.name
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)

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
    raw_score = models.IntegerField(default=0)
    scaled_score = models.IntegerField(default=None, null=True)
    time_finished = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"User: {self.user}, Exam: {self.exam.name}, Section: {self.section.type}, Raw Score: {self.raw_score}"

class Student_Answer(models.Model):
    answer = models.CharField(max_length=100, default="")
    question_number = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    section = models.CharField(max_length=30, default="")
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"User: {self.user}, Exam: {self.exam}, Section: {self.section}, Question: {self.question_number}, Answer: {self.answer}"
