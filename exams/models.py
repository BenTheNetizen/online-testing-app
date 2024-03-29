from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete, pre_save

# Create your models here.

SUCCESS, CANCELLED, NONE = 'SUCCESS', 'CANCELLED', 'NONE'
PAYMENT_STATUS_OPTIONS = [
    (SUCCESS, 'Success'),
    (CANCELLED, 'Cancelled'),
    (NONE, None),
]    

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
    is_premium = models.BooleanField(default=False) # field set to True after user pays
    # payment status set after payment
    payment_status = models.CharField(max_length=9, choices=PAYMENT_STATUS_OPTIONS, default=NONE, null=True)  

    def __str__(self):
        return f'{self.user.username} Profile, Premium: {self.is_premium}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

#model for an exam instance
class ExamInstance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    is_extended_time = models.BooleanField(default=False)

class Section(models.Model):
    name = models.CharField(max_length=100, default=" ")
    #Type = "Reading", "Writing", "Math1", "Math2" for SAT
    #Type = "english", "math", "reading", "science" for ACT
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
