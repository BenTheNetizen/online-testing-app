from django.shortcuts import render
from .models import Section, Exam
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer, Result, Student_Answer
#from results.models import Result
# Create your views here.

#def exam_view(request, pk):
#    exam = Exam.objects.get(pk=pk)
#    return render(request, 'exams/exam.html', {'exam': exam})

def index(request):
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
    print(request.POST)
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
        section = Section.objects.get(type=section_name, exam=pk)
        exam = Exam.objects.get(pk=pk)
        print('EXAM: ' + str(exam))

        for q in questions:
            answer_selected = request.POST.get(q.text)

            #checks if non-Null answer and adds 1 to score if the answer is correct
            if answer_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:

                    if answer_selected == a.text:
                        print("a-text: " + a.text)
                        print("a-letter: " + a.letter)
                        print("q-number: " + str(q.question_number))
                        print("exam-number: " + str(pk))
                        print("section_name: " + section_name)
                        print("user: " + str(user))
                        Student_Answer.objects.create(answer=a.letter, question_number=q.question_number, section=section_name, exam=exam, user=user)
            else:
                print("did not select an answer")

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
