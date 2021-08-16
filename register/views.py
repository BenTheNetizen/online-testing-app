from django.shortcuts import render, redirect
from .forms import UserRegisterForm, StudentRegisterForm
from exams.models import Student

# Create your views here.
def register(request):
    print("REGISTERING ACCOUNT")
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        student_form = StudentRegisterForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            import pdb; pdb.set_trace()
            user = user_form.save()
            user.refresh_from_db()
            student = Student.objects.create(user=user)
            student_form = StudentRegisterForm(request.POST, instance=student)
            student_form.full_clean()
            student_form.save()
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
