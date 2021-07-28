from django.shortcuts import render
from .models import Section, Exam, SectionInstance
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer, Result, Student_Answer
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import csv, io, re, datetime, math
from openpyxl import load_workbook
#from results.models import Result
# Create your views here.
from django.utils.decorators import method_decorator


@login_required
def file_upload(request):
    if request.method == 'POST':

        questions_file = request.FILES['questions_file']
        reading_passages = request.FILES.getlist('reading_passages')
        writing_passages = request.FILES.getlist('writing_passages')
        nocalc_materials = request.FILES.getlist('nocalc_materials')
        calc_materials = request.FILES.getlist('calc_materials')

        #TODO: CANNOT ASSUME THAT THE FILES BEING UPLOADED ARE IN ORDER
        material_files_index = 0
        if not questions_file.name.endswith('.xls') and not questions_file.name.endswith('.xlsx'):
            return render(request, 'exams/file_upload.html', {'error': 'You did not upload a valid Excel file.'})

        wb = load_workbook(filename=request.FILES['questions_file'].file)
        worksheet = wb["Sheet1"]

        #processing variables
        exam_name = ''
        current_section = ''
        question_number = 1
        num_passages = 0

        #TODO FIX THE SAME QUESTION TEXT ERROR
        no_question_index = 1
        #Declare object variables to reduce querying to database
        exam_object = None
        section_object = None
        question_object = None

        for row in worksheet.iter_rows(min_row=2):
            #checks if the 'section' column is empty - this is when processing should stop
            if row[1].value is None:
                break

            #create new exam
            #for cell in row:
                #print(cell.value)
            if question_object is None:
                exam_name = row[0].value
                if Exam.objects.filter(name=exam_name).count() > 0:
                    Exam.objects.get(name=exam_name).delete()

                exam_object, created = Exam.objects.get_or_create(
                    name = exam_name
                )

            #update the previous section's num_passage field
            if section_object is not None:
                section_object.num_passages = num_passages
                section_object.save()
                num_passages = 0

            #if we have a new section, then we create a new section
            if current_section != row[1].value:
                current_section = row[1].value
                num_questions = 0
                time = 0
                #resets the question_number to 1 for a new section
                question_number = 1
                section_name = None

                if current_section == 'reading':
                    num_questions = 52
                    time = 65
                    section_name = 'Reading'
                elif current_section == 'writing':
                    num_questions = 44
                    time = 35
                    section_name = 'Writing and Language'
                elif current_section == 'math1':
                    num_questions = 20
                    time = 25
                    section_name = 'Math (No calculator)'
                elif current_section =='math2':
                    num_questions = 38
                    time = 55
                    section_name = 'Math (Calculator)'
                section_object, created = Section.objects.get_or_create(
                    name = section_name,
                    type = current_section,
                    exam = exam_object,
                    num_questions = num_questions,
                    time = time,
                )


            #create questions
            question_text = row[3].value

            if question_text is not None:
                question_text = question_text.replace('"', '&quot;')
            else:
                question_text = "no question" + str(no_question_index)
                no_question_index += 1


            question_text = question_text.replace("\n", "\\n")
            question_passage = row[2].value
            correct_answer = row[8].value

            if question_passage is not None:
                if question_passage > num_passages:
                    num_passages = question_passage

            question_object, created = Question.objects.get_or_create(
                question_number = question_number,
                text = question_text,
                section = section_object,
                passage = question_passage,
                correct_answer = correct_answer,
                exam = exam_object,

            )
            question_number += 1

            #create answers to question
            answer_object_A, created = Answer.objects.get_or_create(
                text = row[4].value,
                letter = 'A',
                question = question_object
            )

            answer_object_B, created = Answer.objects.get_or_create(
                text = row[5].value,
                letter = 'B',
                question = question_object
            )

            answer_object_C, created = Answer.objects.get_or_create(
                text = row[6].value,
                letter = 'C',
                question = question_object
            )

            answer_object_D, created = Answer.objects.get_or_create(
                text = row[7].value,
                letter = 'D',
                question = question_object
            )


        #assign images to the respective questions in each section
        #NOTE: for reading passages, the image should be representative of the entire passage
        for file in reading_passages:
            filename = file.name
            passage_num = int(re.findall(r'\d+', filename)[0])
            section_object = Section.objects.get(type='reading', exam=exam_object)
            question_object = Question.objects.filter(section=section_object, passage=passage_num).order_by('question_number')[0]
            question_object.material = file
            question_object.save()

        for file in writing_passages:
            filename = file.name
            passage_num = int(re.findall(r'\d+', filename)[0])
            section_object = Section.objects.get(type='writing', exam=exam_object)
            question_object = Question.objects.filter(section=section_object, passage=passage_num).order_by('question_number')[0]
            question_object.material = file
            question_object.save()

        for file in nocalc_materials:
            filename = file.name
            question_no = int(re.findall(r'\d+', filename)[0])
            section_object = Section.objects.get(type='math1', exam=exam_object)
            question_object = Question.objects.get(question_number=question_no, section=section_object)
            question_object.material = file
            question_object.save()

        for file in calc_materials:
            filename = file.name
            question_no = int(re.findall(r'\d+', filename)[0])
            section_object = Section.objects.get(type='math2', exam=exam_object)
            question_object = Question.objects.get(question_number=question_no, section=section_object)
            question_object.material = file
            question_object.save()

    return render(request, 'exams/file_upload.html', {'success': 'Exam successfully uploaded to database.'})

def index(request):
    print(request.user)
    return render(request, 'index.html', {})

@login_required
def exam_list_view(request):
    exams = Exam.objects.all()

    context = {
        'exams':exams,
    }
    return render(request, 'exams/exam_list.html', context)

def exam_list_data_view(request, pk):

    exam = Exam.objects.get(pk=pk)
    sections = exam.get_sections()
    user = request.user
    results = Result.objects.filter(exam=exam, user=user)


    data = []

    # Appending the raw scores
    """
    if results.exists() > 0:
        for result in results:
            raw_scores.append({result.section.type: result.score})
    """

    for section in sections:
        minutes = None
        seconds = None
        score = None
        if SectionInstance.objects.filter(user=user, exam=exam, section=section).exists():
            section_instance = SectionInstance.objects.get(user=user, exam=exam, section=section)
            minutes = section_instance.minutes_left
            seconds = section_instance.seconds_left
        if Result.objects.filter(user=user, exam=exam, section=section).exists():
            result = Result.objects.get(user=user, exam=exam, section=section)
            score = result.score

        data.append({section.type: [score, minutes, seconds]})

    return JsonResponse({
        'data': data,
    })

def start_exam_view(request, pk):
    exam = Exam.objects.get(pk=pk)
    context = {
        'exam':exam,
    }
    return render(request, 'exams/start_exam.html', context)

def section_directions_view(request, pk, section_name):
    exam = Exam.objects.get(pk=pk)
    section = Section.objects.get(exam=exam, type=section_name)
    context = {
        'exam':exam,
        'section':section,
    }
    return render(request, 'exams/section_directions.html', context)

def save_timer_view(request, pk, section_name):

    data = request.POST
    section = Section.objects.get(exam_id=pk, type=section_name)
    exam = Exam.objects.get(pk=pk)
    user = request.user

    section_instance = SectionInstance.objects.get(user=user, exam=exam, section=section)
    section_instance.minutes_left = data['minutes']
    section_instance.seconds_left = data['seconds']
    section_instance.save()

    return JsonResponse({})

def section_view(request, pk, section_name):
    section = Section.objects.get(exam_id=pk, type=section_name)
    exam = Exam.objects.get(pk=pk)
    questions = section.get_questions()
    user = request.user
    minutes_remaining = None
    seconds_remaining = None

    if SectionInstance.objects.filter(user=user, exam=exam, section=section).exists():
        section_instance = SectionInstance.objects.get(user=user, exam=exam, section=section)
        minutes_remaining = section_instance.minutes_left
        seconds_remaining = section_instance.seconds_left
    else:
        section_minutes = section.time
        time_object = SectionInstance.objects.create(user=user, exam=exam, section=section, minutes_left = section_minutes, seconds_left = 0)
        minutes_remaining = section.time
        seconds_remaining = 0

    context = {
        'section':section,
        'exam':exam,
        'questions':questions,
        'minutes_remaining': minutes_remaining,
        'seconds_remaining': seconds_remaining,
    }

    if section_name == 'math1' or section_name =='math2':
        template = 'exams/math_section.html'
    else:
        template = 'exams/passage_section.html'

    return render(request, template, context)

def section_math_data_view(request, pk, section_name):
    # CURRENTLY HANDLES RETIEVING DATA FOR THE MATH SECTION
    section = Section.objects.get(exam=pk, type=section_name)
    exam = Exam.objects.get(pk=pk)
    user = request.user

    image_urls = []

    data = []
    #gives key, value pairs to "questions," which are the questions and the answers
    for q in section.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)

        # ERROR OCCURS WHEN UNCOMMENTED
        #if 'no question' in q.text:
        #    q.text = ''

        # Get's the previously answered question if possible
        student_answer = Student_Answer.objects.filter(user=user, exam=exam, section=section_name, question_number=q.question_number).first()
        student_answer_text = None

        if student_answer is not None and student_answer.answer != 'N':
            student_answer_text = Answer.objects.get(question=q, letter=student_answer.answer).text

        #GETS THE IMAGE URLS
        image_url = None

        if q.material.name:
            image_url = q.material.url
        data.append({str(q): [answers, student_answer_text, image_url]})

    return JsonResponse({
        'data': data,
        'time': section.time,
        'img_urls': image_urls,
        'section': section.type,
    })

def section_passage_data_view(request, pk, section_name, passage_num):
    section = Section.objects.get(exam=pk, type=section_name)
    exam = Exam.objects.get(pk=pk)
    user = request.user

    image_urls = []
    if section_name == 'reading' or section_name == 'writing':
        image = Question.objects.filter(section=section, passage=passage_num).order_by('question_number')[0].material
        # MAKES SURE THAT A URL EXISTS
        if image.name != '':
            image_urls.append(image.url)

    if section_name == 'math1' or section_name == 'math2':
        for question in section.get_questions():
            if question.material.name:
                image_urls.append(question.material.url)

    questions = []
    #gives key, value pairs to "questions," which are the questions and the answers
    for q in Question.objects.filter(exam=exam, section=section, passage=passage_num):
        answers = []
        for a in q.get_answers():
            answers.append(a.text)

        # ERROR OCCURS WHEN UNCOMMENTED
        #if 'no question' in q.text:
        #    q.text = ''

        # Get's the previously answered question if possible
        student_answer = Student_Answer.objects.filter(user=user, exam=exam, section=section_name, question_number=q.question_number).first()
        student_answer_text = None

        if student_answer is not None and student_answer.answer != 'N':
            student_answer_text = Answer.objects.get(question=q, letter=student_answer.answer).text
        questions.append({q.question_number: [str(q), answers, student_answer_text]})

    return JsonResponse({
        'data': questions,
        'time': section.time,
        'img_urls': image_urls,
        'section': section.type,
    })

def section_break_view(request, pk, break_num):
    if break_num == 1:
        return render(request, 'exams/break1.html', {})
    elif break_num == 2:
        return render(request, 'exams/break2.html', {})

def save_section_view(request, pk, section_name):
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
        raw_score = 0

        student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section_name)
        questions = Question.objects.filter(exam=exam, section=section)

        for question in questions:
            if Student_Answer.objects.filter(user=user, exam=exam, section=section_name, question_number=question.question_number).exists():
                answer_letter = Student_Answer.objects.get(user=user, exam=exam, section=section_name, question_number=question.question_number).answer
                if answer_letter == question.correct_answer:
                    raw_score += 1
            else:
                Student_Answer.objects.create(user=user, exam=exam, section=section_name, question_number=question.question_number, answer='N')

        #CREATE SECTION RESULT OBJECT
        Result.objects.create(section=section, user=user, exam=exam, score=raw_score)

    return JsonResponse({'section_name':section_name})

def save_question_view(request, pk, section_name):
    print("received request")

    if request.is_ajax():

        data = request.POST
        #converts the data from a QueryDict to a dict
        data_ = dict(data.lists())

        user = request.user

        exam = Exam.objects.get(pk=pk)
        section = Section.objects.get(type=section_name, exam=pk)

        #CONVERT THE QUOTATION ESCAPES BACK TO REGULAR QUOTES
        question_text = data['question'].replace('"', '&quot;')
        question = Question.objects.get(text=question_text, section=section)
        answer_letter = Answer.objects.get(question=question, text=data['answer']).letter

        # Checks if there has already been an answer to the question and updates if true, otherwise created the student_answer object
        if Student_Answer.objects.filter(user=user, exam=exam, section=section_name, question_number=question.question_number).exists():
            student_answer = Student_Answer.objects.get(question_number=question.question_number, section=section_name, exam=exam, user=user)
            student_answer.answer = answer_letter
            student_answer.save()
        else:
            Student_Answer.objects.create(
                answer = answer_letter,
                question_number = question.question_number,
                section = section_name,
                exam = exam,
                user = user,
        )
        print("CREATED STUDENT ANSWER OBJECT")
    return JsonResponse({
        'hello':'hello'
    })
