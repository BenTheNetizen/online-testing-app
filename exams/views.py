from django.shortcuts import render
from .models import Section, Exam
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer, Result, Student_Answer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv, io
from openpyxl.reader.excel import load_workbook
#from results.models import Result
# Create your views here.

@login_required
def file_upload(request):
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        file = request.FILES['file']
        if not file.name.endswith('.xls') or not file.name.endswish('.xlsx'):
            messages.error(request, 'This is not an Excel file')

        wb = load_workbook(filename=request.FILES['file'].file)
        worksheet = wb["Sheet1"]

        #processing variables
        exam_name = ''
        current_section = ''
        question_number = 1

        #Declare object variables to reduce querying to database
        exam_object = None
        section_object = None
        question_object = None

        #import pdb; pdb.set_trace()
        for row in worksheet.iter_rows(min_row=2):
            #checks if the 'section' column is empty - this is when processing should stop
            if row[1].value is None:
                break

            #create new exam
            for cell in row:
                print(cell.value)
            if question_object is None:
                exam_name = row[0].value
                exam_object, created = Exam.objects.get_or_create(
                    name = exam_name
                )
            #if we have a new section, then we create a new section
            if current_section != row[1].value:
                current_section = row[1].value
                num_questions = 0
                time = 0
                #resets the question_number to 1
                question_number = 1
                if current_section == 'reading':
                    num_questions = 52
                    time = 65
                elif current_section == 'writing':
                    num_questions = 44
                    time = 35
                elif current_section == 'math1':
                    num_questions = 20
                    time = 25
                elif current_section =='math2':
                    num_questions = 38
                    time = 55
                section_object, created = Section.objects.get_or_create(
                    name = current_section,
                    type = current_section,
                    exam = exam_object,
                    num_questions = num_questions,
                    time = time,
                )

            #exam_object = Exam.objects.get(name = exam_name)
            #current_section_object = Section.objects.get(type = current_section, exam = exam_object)

            #create questions and answers
            question_text = row[2].value
            if question_text is None:
                question_text = "no question"
            question_object, created = Question.objects.get_or_create(
                question_number = question_number,
                text = question_text,
                section = section_object,
            )
            question_number += 1

            answer_object_A, created = Answer.objects.get_or_create(
                text = row[3].value,
                letter = 'A',
                question = question_object
            )

            answer_object_B, created = Answer.objects.get_or_create(
                text = row[4].value,
                letter = 'B',
                question = question_object
            )

            answer_object_C, created = Answer.objects.get_or_create(
                text = row[5].value,
                letter = 'C',
                question = question_object
            )

            answer_object_D, created = Answer.objects.get_or_create(
                text = row[6].value,
                letter = 'D',
                question = question_object
            )

    return render(request, 'exams/file_upload.html')

def index(request):
    print(request.user)
    return render(request, 'index.html', {})

def test(request, pk):
    return render(request, 'index.html', {})

class ExamListView(ListView):
    model=Exam
    template_name = 'exams/exam_list.html'

def section_view(request, pk, section_name):
    section = Section.objects.get(exam_id=pk, type=section_name)
    return render(request, 'exams/section.html', {'section': section})

def section_data_view(request, pk, section_name):
    section = Section.objects.get(exam=pk, type=section_name)
    questions = []
    #gives key, value pairs to "questions," which are the questions and the answers
    for q in section.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})

    return JsonResponse({
        'data': questions,
        'time': section.time,
    })

def section_break_view(request, pk, break_num):
    if break_num == 1:
        return render(request, 'exams/break1.html', {})
    elif break_num == 2:
        return render(request, 'exams/break2.html', {})

def save_section_view(request, pk, section_name):
    #import pdb; pdb.set_trace()
    print(request.POST)
    if request.is_ajax():

        data = request.POST
        #converts the data from a QueryDict to a dict
        data_ = dict(data.lists())
        #gets rid of the csrf token from the dict
        data_.pop('csrfmiddlewaretoken')

        #grabs the questions and section displayed on the site
        user = request.user
        print('USER: ' + str(user))
        section = Section.objects.get(type=section_name, exam=pk)
        questions = section.get_questions()
        exam = Exam.objects.get(pk=pk)
        print('EXAM: ' + str(exam))
        #import pdb; pdb.set_trace()
        for q in questions:
            answer_selected = request.POST.get(q.text)
            print(answer_selected)
            #checks if non-Null answer and adds 1 to score if the answer is correct
            if answer_selected != 'N':
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:

                    if answer_selected == a.text:
                        print("a-text: " + a.text)
                        print("a-letter: " + a.letter)
                        print("q-number: " + str(q.question_number))
                        print("exam-number: " + str(pk))
                        print("section_name: " + section_name)
                        print("user: " + str(user))
                        print("CREATED STUDENT ANSWER OBJECT")
                        Student_Answer.objects.create(answer=a.letter, question_number=q.question_number, section=section_name, exam=exam, user=user)

            else:
                print("CREATED NULL STUDENT ANSWER")
                Student_Answer.objects.create(answer='N', question_number=q.question_number, section=section_name, exam=exam, user=user)

    return JsonResponse({'section_name':section_name})



"""
def save_section_view(request, pk, section_name):
    #print(request.POST)

    results = []
    score = 0
    if request.is_ajax():

        data = request.POST
        #converts the data from a QueryDict to a dict
        data_ = dict(data.lists())
        #gets rid of the csrf token from the dict
        data_.pop('csrfmiddlewaretoken')

        #grabs the questions displayed on the site
        #THIS IS NECESSARY IF THE QUESTIONS ARE DISPLAYED IN RANDOM ordering
        #probably could delete and instead use section.get_questions
        questions = []
        for k in data_.keys():
            print('key: ', k)
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        print('USER: ' + str(user))
        section = Section.objects.get(pk=pk)


        multiplier = 100 / section.num_questions

        correct_answer = None

        for q in questions:
            answer_selected = request.POST.get(q.text)

            #checks if non-Null answer and adds 1 to score if the answer is correct
            if answer_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if answer_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append({str(q): {'correct_answer': correct_answer,
                                         'answered': answer_selected}})
            else:
                results.append({str(q): 'not answered'})

        score = score * multiplier
        Result.objects.create(section=section, user=user, score=score)

    return JsonResponse({'score': score, 'results': results, 'section_name': section_name})
"""
