from django.shortcuts import render
from .models import Section, Exam
from django.views.generic import ListView
from django.http import JsonResponse
from questions.models import Question, Answer
from results.models import Result
# Create your views here.

class ExamListView(ListView):
    model=Exam
    #template_name = 'exams/main.html'

class SectionListView(ListView):
    model=Section
    template_name = 'exams/main.html'

def exam_view(request, pk):
    exam = Exam.objects.get(pk=pk)
    return render(request, 'exams/exam.html', {'exam': exam})

def section_view(request, pk):
    section = Section.objects.get(pk=pk)
    return render(request, 'exams/section.html', {'section': section})

def section_data_view(request, pk):
    section = Section.objects.get(pk=pk)
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

def save_section_view(request, pk):
    #print(request.POST)
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

        score = 0
        multiplier = 100 / section.num_questions
        results = []
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

        score_ = score * multiplier
        Result.objects.create(section=section, user=user, score=score_)


    return JsonResponse({'score': score_, 'results': results})
