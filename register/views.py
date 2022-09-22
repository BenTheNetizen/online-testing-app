from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from .forms import UserRegisterForm, StudentRegisterForm, PasswordResetForm
from exams.models import Student
from .models import StudentAccessCode

# Create your views here.
def register(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        student_form = StudentRegisterForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()
            student = Student.objects.create(user=user)
            student_form = StudentRegisterForm(request.POST, instance=student)
            student_form.full_clean()
            # Give student premium if the student_access_code is correct 
            all_codes = StudentAccessCode.objects.all()
            for code in all_codes:
                if code.code == student_form.instance.student_access_code:
                    student_form.instance.is_premium = True
            student_form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('exams:exam-list-view')
            #return render(request, 'register/register.html', {'form':form})
            #import pdb; pdb.set_trace()
        #return redirect("/")
    else:
        user_form = UserRegisterForm()
        student_form = StudentRegisterForm()

    return render(request, 'register/register.html', {
        'user_form':user_form,
        'student_form':student_form,})

def password_reset(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            print('Email: ' + str(email))
            return redirect('exams:exam-list-view')
    else:
        password_reset_form = PasswordResetForm()

    return render(request, 'registration/password_reset.html', {
        'form':password_reset_form,
        })
