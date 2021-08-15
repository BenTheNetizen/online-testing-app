from django.shortcuts import render
from django.conf import settings
# Create your views here.
import os
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from questions.models import Student_Answer, Question, Result
from exams.models import Exam, Section
from openpyxl import load_workbook
from easy_pdf.views import PDFTemplateView
import easy_pdf
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


    template_path = 'results/pdf-of-results.html'
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

def render_pdf_of_results(request, pk):
    user = request.user
    exam = Exam.objects.get(pk=pk)
    sections = exam.get_sections()
    raw_reading_score, raw_writing_score, raw_math1_score, raw_math2_score = None, None, None, None
    omitted_reading, omitted_writing, omitted_math1, omitted_math2 = None, None, None, None
    reading_questions, writing_questions, math1_questions, math2_questions = None, None, None, None
    reading_student_answers, writing_student_answers, math1_student_answers, math2_student_answers = None, None, None, None

    for section in sections:
        if (section.type == 'reading'):
            raw_reading_score = Result.objects.get(user=user, exam=exam, section=section).score
            omitted_reading = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
            reading_questions = Question.objects.filter(exam=exam, section=section)
            reading_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).values_list('answer', flat=True)
        elif (section.type == 'writing'):
            raw_writing_score = Result.objects.get(user=user, exam=exam, section=section).score
            omitted_writing = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
            writing_questions = Question.objects.filter(exam=exam, section=section)
            writing_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).values_list('answer', flat=True)
        elif (section.type == 'math1'):
            raw_math1_score = Result.objects.get(user=user, exam=exam, section=section).score
            omitted_math1 = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
            math1_questions = Question.objects.filter(exam=exam, section=section)
            math1_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).values_list('answer', flat=True)
        elif (section.type == 'math2'):
            raw_math2_score = Result.objects.get(user=user, exam=exam, section=section).score
            omitted_math2 = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
            math2_questions = Question.objects.filter(exam=exam, section=section)
            math2_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).values_list('answer', flat=True)

    reading_score = 400 - (10 * (52 - raw_reading_score))
    reading_score = 100 if reading_score < 100 else reading_score

    writing_score = 400 - (20 * (44 - raw_writing_score))
    writing_score = 100 if writing_score < 100 else writing_score

    raw_math_score = raw_math1_score + raw_math2_score
    math_score = 800 - (15 * (58 - raw_math_score))
    math_score = 200 if math_score < 200 else math_score

    total_score = reading_score + writing_score + math_score

    incorrect_reading = 52 - (omitted_reading + raw_reading_score)
    incorrect_writing = 44 - (omitted_writing + raw_writing_score)
    incorrect_math1 = 25 - (omitted_math1 + raw_math1_score)
    incorrect_math2 = 38 - (omitted_math1 + raw_math2_score)

    reading_questions_answers = zip(reading_questions, reading_student_answers)
    writing_questions_answers = zip(writing_questions, writing_student_answers)
    math1_questions_answers = zip(math1_questions, math1_student_answers)
    math2_questions_answers = zip(math2_questions, math2_student_answers)

    context = {
        'exam':exam,
        'raw_reading_score':raw_reading_score,
        'raw_writing_score':raw_writing_score,
        'raw_math1_score':raw_math1_score,
        'raw_math2_score':raw_math2_score,
        'omitted_reading':omitted_reading,
        'omitted_writing':omitted_writing,
        'omitted_math1':omitted_math1,
        'omitted_math2':omitted_math2,
        'reading_questions':reading_questions,
        'writing_questions':writing_questions,
        'math1_questions':math1_questions,
        'math2_questions':math2_questions,
        'reading_student_answers':reading_student_answers,
        'writing_student_answers':writing_student_answers,
        'math1_student_answers':math1_student_answers,
        'math2_student_answers':math2_student_answers,
        'incorrect_reading':incorrect_reading,
        'incorrect_writing':incorrect_writing,
        'incorrect_math1':incorrect_math1,
        'incorrect_math2':incorrect_math2,
        'reading_score':reading_score,
        'writing_score':writing_score,
        'math_score':math_score,
        'total_score':total_score,
        'reading_questions_answers':reading_questions_answers,
        'writing_questions_answers':writing_questions_answers,
        'math1_questions_answers':math1_questions_answers,
        'math2_questions_answers':math2_questions_answers,
    }

    return easy_pdf.rendering.render_to_pdf_response(request, 'results/pdf-of-results.html', context, using=None, download_filename=None, content_type='application/pdf', response_class=HttpResponse)

def render_pdf_of_results2(request, pk):
    import pdb; pdb.set_trace()
    user = request.user
    exam = Exam.objects.get(pk=pk)

    exam_name = exam.name

    context = {'test': 'testvalue2', 'test2': 'testvalue2'}
    return easy_pdf.rendering.render_to_pdf_response(request, 'results/pdf-of-results.html', context, using=None, download_filename=None, content_type='application/pdf', response_class=HttpResponse)
