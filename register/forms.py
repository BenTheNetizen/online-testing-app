from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from exams.models import Student
#to add more fields to the registration form, add more attributes and update the 'fields' property in class Meta
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['parent_name', 'parent_email', 'parent_phone_number', 'student_access_code']
    #parent_name = forms.CharField(max_length=30, required=False, help_text="")
    #parent_email = forms.CharField(max_length=30, required=True, help_text="")
    #parent_phone_number = forms.CharField(max_length=30, required=False, help_text="")
    #student_access_code = forms.CharField(max_length=30, required=False, help_text="")
    #email = forms.EmailField(max_length=254, help_text='')
