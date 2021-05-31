from django.shortcuts import render
from django.conf import settings
# Create your views here.
import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from questions.models import Student_Answer
from exams.models import Exam, Section
from openpyxl import load_workbook
import os

def results(request, pk):
    user = request.user
    print(user)
    print(user.email)
    return render(request, 'results/results.html', {})

def render_pdf_view(request, pk):
    module_dir = os.path.dirname(__file__) #get current directory
    file_path = os.path.join(module_dir, 'scoring_sheets/test-scoring-template.xlsx')

    wb = load_workbook(filename=file_path)
    worksheet = wb["Sheet1"]

    exam = Exam.objects.get(pk=pk)
    section_object = None
    question_number = 1
    key = None
    user = request.user
    num_correct = 0
    num_wrong = 0
    num_unanswered = 0
    #IF THE USER WENT THROUGH THE EXAM WITHOUT REPEATING ANY ANSWERS, 'answers' IS INDEXED IN ORDER OF QUESTION NUMBER AND SECTION
    answers = Student_Answer.objects.filter(user=user, exam=exam).values()
    for row in worksheet.iter_rows(min_row=2):
        #import pdb; pdb.set_trace()
        question_number = row[2].value
        question_index = row[1].value
        section_object = Section.objects.get(exam=exam, type=row[3].value)
        key = row[4].value
        #subtract 1 for the 0 based indexing
        if answers[question_index]['answer'] == key:
            num_correct += 1
        elif answers[question_index]['answer'].upper() == 'N':
            num_unanswered += 1
        else:
            num_wrong += 1


    template_path = 'results/test.html'
    context = {'myvar': 'this is your template context',
               'correct': num_correct,
               'unanswered': num_unanswered,
               'wrong': num_wrong,
               }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # if download:
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if display:
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
