from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

#to add more fields to the registration form, add more attributes and update the 'fields' property in class Meta
class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name*'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your Email*'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Password*'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Confirm Password*'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
