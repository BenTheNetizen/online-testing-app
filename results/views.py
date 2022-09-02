from django.shortcuts import render
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import ordinal
# Create your views here.
import os
from django.http import HttpResponse
from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from questions.models import Student_Answer, Question, Result
from exams.models import Exam, Section, User
from openpyxl import load_workbook
from datetime import date
import numpy as np
import pandas as pd
#from easy_pdf.views import PDFTemplateView
#import easy_pdf
import os
import math


def results(request, pk):
    user = request.user
    print(user)
    print(user.email)
    return render(request, 'results/results.html', {})

def render_pdf_view(request, pk, username):
    user = User.objects.get(username=username)
    exam = Exam.objects.get(pk=pk)
    exam_type = exam.type
    sections = exam.get_sections()
    current_date = date.today().strftime("%m/%d/%Y")

    # Get student name if there is an underscore in username
    user_name = None
    if '_' in username:
        user_name = username.split('_')
        user_name = user_name[0] + ' ' + user_name[1]
        user_name = user_name.title()
    else:
        user_name = username

    # IM REUSING 'reading' FOR BOTH THE ACT AND SAT TESTS
    raw_reading_score, raw_writing_score, raw_math1_score, raw_math2_score, raw_english_score, raw_math_score, raw_science_score = None, None, None, None, None, None, None
    omitted_reading, omitted_writing, omitted_math1, omitted_math2, omitted_english, omitted_math, omitted_science = None, None, None, None, None, None, None
    reading_questions, writing_questions, math1_questions, math2_questions, english_questions, math_questions, science_questions = None, None, None, None, None, None, None
    reading_student_answers, writing_student_answers, math1_student_answers, math2_student_answers, english_student_answers, math1_student_answers, science_student_answers = None, None, None, None, None, None, None
    reading_score, writing_score, math1_score, math2_score, english_score, math_score, science_score = None, None, None, None, None, None, None
    for section in sections:
        if exam_type == 'SAT':
            if (section.type == 'reading'):
                raw_reading_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                reading_score = Result.objects.get(user=user, exam=exam, section=section).scaled_score
                omitted_reading = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                reading_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                reading_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).values_list('answer', flat=True)
            elif (section.type == 'writing'):
                raw_writing_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                writing_score = Result.objects.get(user=user, exam=exam, section=section).scaled_score
                omitted_writing = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                writing_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                writing_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
            elif (section.type == 'math1'):
                raw_math1_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                math1_score = Result.objects.get(user=user, exam=exam, section=section).scaled_score
                omitted_math1 = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                math1_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                math1_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
            elif (section.type == 'math2'):
                raw_math2_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                math2_score = Result.objects.get(user=user, exam=exam, section=section).scaled_score
                omitted_math2 = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                math2_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                math2_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
        elif exam_type == 'ACT':
            if (section.type == 'english'):
                raw_english_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                english_score = Result.objects.get(user=user, exam=exam, section=section).scaled_score
                omitted_english = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                english_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                english_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
            elif (section.type == 'math'):
                raw_math_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                math_score = Result.objects.get(user=user, exam=exam, section=section).scaled_score
                omitted_math = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                math_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                math_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
            elif (section.type == 'reading'):
                raw_reading_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                reading_score = Result.objects.get(user=user, exam=exam, section=section).scaled_score
                omitted_reading = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                reading_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                reading_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
            elif (section.type == 'science'):
                raw_science_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                science_score = Result.objects.get(user=user, exam=exam, section=section).scaled_score
                omitted_science = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                science_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                science_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
        elif exam_type == 'DIAGNOSTIC':
            if (section.type == 'reading'):
                raw_reading_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                omitted_reading = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                reading_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                reading_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
            elif (section.type == 'writing'):
                raw_writing_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                omitted_writing = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                writing_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                writing_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
            elif (section.type == 'math1'):
                raw_math1_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                omitted_math1 = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                math1_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                math1_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
            elif (section.type == 'math2'):
                raw_math2_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                omitted_math2 = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                math2_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                math2_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
            elif (section.type == 'english'):
                raw_english_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                omitted_english = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                english_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                english_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
            elif (section.type == 'math'):
                raw_math_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                omitted_math = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                math_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                math_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)
            elif (section.type == 'science'):
                raw_science_score = Result.objects.get(user=user, exam=exam, section=section).raw_score
                omitted_science = Student_Answer.objects.filter(user=user, exam=exam, section=section.type, answer='N').count()
                science_questions = Question.objects.filter(exam=exam, section=section).order_by('question_number')
                science_student_answers = Student_Answer.objects.filter(user=user, exam=exam, section=section.type).order_by('question_number').values_list('answer', flat=True)

    if exam_type == 'SAT':
        total_score = reading_score + writing_score + math1_score + math2_score
        math_section_score = math1_score + math2_score
        reading_writing_score = reading_score + writing_score

        incorrect_reading = 52 - (omitted_reading + raw_reading_score)
        incorrect_writing = 44 - (omitted_writing + raw_writing_score)
        incorrect_math1 = 25 - (omitted_math1 + raw_math1_score)
        incorrect_math2 = 38 - (omitted_math2 + raw_math2_score)

        reading_questions_answers = zip(reading_questions, reading_student_answers)
        writing_questions_answers = zip(writing_questions, writing_student_answers)
        math1_questions_answers = zip(math1_questions, math1_student_answers)
        math2_questions_answers = zip(math2_questions, math2_student_answers)

        reading_test_score = int(np.floor(reading_score / 10))
        writing_test_score = int(np.floor(writing_score / 10))
        math_test_score = int(np.floor((math1_score + math2_score) / 20))

        # Get Percentiles
        module_dir = os.path.dirname(__file__) #get current directory
        percentiles_file_path = os.path.join(module_dir, 'data_files/Percentiles.csv')
        percentiles_df = pd.read_csv(percentiles_file_path)
        percentile_index = percentiles_df.loc[percentiles_df['SAT'] == total_score].index[0]
        percentile = percentiles_df['SAT Percentiles'][percentile_index]
        percentile = ordinal(percentile)

        index = percentiles_df.loc[percentiles_df['SAT Math Score'] == math_section_score].index[0]
        math_percentile = percentiles_df['SAT Math Percentiles'][index]
        math_percentile = ordinal(math_percentile)

        index = percentiles_df.loc[percentiles_df['SAT RW Score'] == reading_writing_score].index[0]
        reading_writing_percentile = percentiles_df['SAT RW Percentiles'][index]
        reading_writing_percentile = ordinal(reading_writing_percentile)

        # GET CATEGORY DATA
        questions = Question.objects.filter(exam=exam)
        #reading_vocabulary_questions, structure_questions, inference_questions, graphs_figures_questions, events_questions, fiction_questions, natural_science_questions, social_science_questions, historical_questions = None, None, None, None, None, None, None, None, None
        #agreement_questions, english_vocabulary_questions, parallelism_questions, transition_words_questions, punctuation_questions, common_words_questions, parts_of_speech_questions, sentence_placement_questions, sentence_structure_questions, idioms_questions, redundancy_questions, english_reading_graphs_questions = None, None, None, None, None, None, None, None, None, None, None, None,
        #fundamental_algebra_questions, geometry_questions, ratios_questions, complex_numbers_questions, trigonometry_questions, math_reading_graphs_questions, probability_questions, statistics_questions, logarithsm_questions, miscellaneous_questions = None, None, None, None, None, None, None, None, None, None

        # EACH CATEGORY CORRESPONDS TO A LIST
        # FIRST ELEMENT IN LIST IS THE TOTAL NUMBER OF QUESTIONS IN THAT CATEGORY
        # SECOND ELEMENT IN LIST IS THE NUMBER OF QUESTIONS CORRECT IN THAT CATEGORY
        subscores_category_data = {
            'CM':[0,0,0,None],
            'PSDA':[0,0,0,None],
            'HA':[0,0,0,None],
            'WC':[0,0,0,None],
            'EI':[0,0,0,None],
            'PAM':[0,0,0,None],
            'SEC':[0,0,0,None],
        }
        reading_category_data = {
            'D':[0,0,None],
            'I':[0,0,None],
            'S':[0,0,None],
            'GF':[0,0,None],
            'VC':[0,0,None],
            'F':[0,0,None],
            'NS':[0,0,None],
            'SS':[0,0,None],
            'H':[0,0,None],
            'DP':[0,0,None],
        }
        english_category_data = {
            'A':[0,0,None],
            'P':[0,0,None],
            'ST':[0,0,None],
            'VC':[0,0,None],
            'CW':[0,0,None],
            'ID':[0,0,None],
            'COMP':[0,0,None],
            'PS':[0,0,None],
            'R':[0,0,None],
            'TW':[0,0,None],
            'SP':[0,0,None],
            'RG':[0,0,None],
            'UP':[0,0,None],
            'TS':[0,0,None],
            'SX':[0,0,None],
        }
        math_category_data = {
            'FA':[0,0,None],
            'WP':[0,0,None],
            'VS':[0,0,None],
            'SE':[0,0,None],
            'Q':[0,0,None],
            'FOIL':[0,0,None],
            'AI':[0,0,None],
            'EXP':[0,0,None],
            'GEO':[0,0,None],
            'CR':[0,0,None],
            'TR':[0,0,None],
            '3D':[0,0,None],
            'PL':[0,0,None],
            'RAT':[0,0,None],
            'CN':[0,0,None],
            'TRIG':[0,0,None],
            'RG':[0,0,None],
            'PROB':[0,0,None],
            'STAT':[0,0,None],
            'LOG':[0,0,None],
            'RE':[0,0,None],
            'MISC':[0,0,None],
            'MMM':[0,0,None],
            'FN':[0,0,None],
        }
        category_data = {
            'CM':[0,0, None],
            'PSDA':[0,0,None],
            'HA':[0,0,None],
            'WC':[0,0,None],
            'EI':[0,0,None],
            'PAM':[0,0,None],
            'SEC':[0,0,None],
            'D':[0,0,None],
            'I':[0,0,None],
            'S':[0,0,None],
            'GF':[0,0,None],
            'VC':[0,0,None],
            'F':[0,0,None],
            'NS':[0,0,None],
            'SS':[0,0,None],
            'H':[0,0,None],
            'DP':[0,0,None],
            'A':[0,0,None],
            'P':[0,0,None],
            'ST':[0,0,None],
            'VC':[0,0,None],
            'CW':[0,0,None],
            'ID':[0,0,None],
            'COMP':[0,0,None],
            'PS':[0,0,None],
            'R':[0,0,None],
            'TW':[0,0,None],
            'SP':[0,0,None],
            'RG':[0,0,None],
            'UP':[0,0,None],
            'TS':[0,0,None],
            'SX':[0,0,None],
            'FA':[0,0,None],
            'WP':[0,0,None],
            'SE':[0,0,None],
            'Q':[0,0,None],
            'FOIL':[0,0,None],
            'AI':[0,0,None],
            'EXP':[0,0,None],
            'GEO':[0,0,None],
            'CR':[0,0,None],
            'TR':[0,0,None],
            '3D':[0,0,None],
            'PL':[0,0,None],
            'RAT':[0,0,None],
            'CN':[0,0,None],
            'TRIG':[0,0,None],
            'RG':[0,0,None],
            'PROB':[0,0,None],
            'STAT':[0,0,None],
            'LOG':[0,0,None],
            'RE':[0,0,None],
            'MISC':[0,0,None],
            'MMM':[0,0,None],
            'MC':[0,0,None],
            'FR':[0,0,None],
            'OI':[0,0,None],
        }

        for question in questions:
            category_string = question.categories
            categories = None
            try:
                categories = category_string.split(',')
            except:
                # this case occurs if there is only one category
                categories = [category_string]

            for category in categories:
                if category is None:
                    break 
                category = category.replace(' ', '')

                # handle the subscores category
                if category in subscores_category_data.keys():
                    # Increase the count of the category
                    subscores_category_data[category][0] += 1
                    # If answered correctly, increase the correct count of that category
                    selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                    if selected_answer.is_correct:
                        subscores_category_data[category][1] += 1

                if question.section.type == 'reading':
                    if category in reading_category_data.keys():
                        # Increase the count of the category
                        reading_category_data[category][0] += 1
                        # If answered correctly, increase the correct count of that category
                        selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                        if selected_answer.is_correct:
                            reading_category_data[category][1] += 1
                elif question.section.type == 'writing':
                    if category in english_category_data.keys():
                        # Increase the count of the category
                        english_category_data[category][0] += 1
                        # If answered correctly, increase the correct count of that category
                        selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                        if selected_answer.is_correct:
                            english_category_data[category][1] += 1
                elif question.section.type == 'math1' or question.section.type == 'math2':
                    if category in math_category_data.keys():
                        # Increase the count of the category
                        math_category_data[category][0] += 1
                        # If answered correctly, increase the correct count of that category
                        selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                        if selected_answer.is_correct:
                            math_category_data[category][1] += 1

                if category not in category_data.keys():
                    print(category + ' is not in the category_data dictionary!!!')

        # Loop through the dictionary and perform the percentages computation
        for key in subscores_category_data:
            # NOTE: subscores are out of 15, so we have an additional value in the list
            # Assign 'NA' to categories with 0 appearances
            if subscores_category_data[key][0] == 0:
                subscores_category_data[key][3] = 'NA'
            else:
                # Assign the fraction in proportion to 15
                subscores_category_data[key][3] = int((subscores_category_data[key][1] * 15) / subscores_category_data[key][0])
                # Get percentage from the proportion to 15
                subscores_category_data[key][2] = int((subscores_category_data[key][3] / 15) * 100)

        for key in reading_category_data:
            # Assign 'NA' to categories with 0 appearances
            if reading_category_data[key][0] == 0:
                reading_category_data[key][2] = 'NA'
                # WE ARE SETTING THIS EQAUL TO 0 FOR NOW
                reading_category_data[key][2] = 0
            else:
                # Assign the percentage to the third element in the value list
                reading_category_data[key][2] = int((reading_category_data[key][1] / reading_category_data[key][0]) * 100)

        for key in english_category_data:
            # Assign 'NA' to categories with 0 appearances
            if english_category_data[key][0] == 0:
                english_category_data[key][2] = 'NA'
                # WE ARE SETTING THIS EQAUL TO 0 FOR NOW
                english_category_data[key][2] = 0
            else:
                # Assign the percentage to the third element in the value list
                english_category_data[key][2] = int((english_category_data[key][1] / english_category_data[key][0]) * 100)

        for key in math_category_data:
            # Assign 'NA' to categories with 0 appearances
            if math_category_data[key][0] == 0:
                math_category_data[key][2] = 'NA'
                # WE ARE SETTING THIS EQAUL TO 0 FOR NOW
                math_category_data[key][2] = 0
            else:
                # Assign the percentage to the third element in the value list
                math_category_data[key][2] = int((math_category_data[key][1] / math_category_data[key][0]) * 100)

        context = {
            'exam':exam,
            'user': user,
            'user_name': user_name,
            'current_date':current_date,
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
            'math1_score':math1_score,
            'math2_score':math2_score,
            'total_score':total_score,
            'reading_questions_answers':reading_questions_answers,
            'writing_questions_answers':writing_questions_answers,
            'math1_questions_answers':math1_questions_answers,
            'math2_questions_answers':math2_questions_answers,
            'test_questions_answers':reading_questions_answers,
            'reading_test_score': reading_test_score,
            'writing_test_score': writing_test_score,
            'math_test_score': math_test_score,
            'subscores_category_data':subscores_category_data,
            'reading_category_data':reading_category_data,
            'english_category_data':english_category_data,
            'math_category_data':math_category_data,
            'percentile':percentile,
            'math_percentile':math_percentile,
            'reading_writing_percentile':reading_writing_percentile,
        }

        return render(request, 'results/sat-results.html', context)
        #return render(request, 'results/og-score-report.html', context)

    elif exam_type == 'ACT':
        total_score = (english_score + math_score + reading_score + science_score) // 4

        incorrect_english = 75 - (omitted_english + raw_english_score)
        incorrect_math = 60 - (omitted_math + raw_math_score)
        incorrect_reading = 40 - (omitted_reading + raw_reading_score)
        incorrect_science = 40 - (omitted_science + raw_science_score)

        english_questions_answers = zip(english_questions, english_student_answers)
        math_questions_answers = zip(math_questions, math_student_answers)
        reading_questions_answers = zip(reading_questions, reading_student_answers)
        science_questions_answers = zip(science_questions, science_student_answers)

        # Get Percentiles
        module_dir = os.path.dirname(__file__) #get current directory
        percentiles_file_path = os.path.join(module_dir, 'data_files/Percentiles.csv')
        percentiles_df = pd.read_csv(percentiles_file_path)
        percentile_index = percentiles_df.loc[percentiles_df['ACT'] == total_score].index[0]
        percentile = percentiles_df['ACT Percentiles'][percentile_index]
        percentile = ordinal(percentile)

        index = percentiles_df.loc[percentiles_df['ACT English'] == english_score].index[0]
        english_percentile = percentiles_df['ACT English Percentiles'][index]
        english_percentile = ordinal(english_percentile)

        index = percentiles_df.loc[percentiles_df['ACT Math'] == math_score].index[0]
        math_percentile = percentiles_df['ACT Math Percentiles'][index]
        math_percentile = ordinal(math_percentile)

        index = percentiles_df.loc[percentiles_df['ACT Reading'] == reading_score].index[0]
        reading_percentile = percentiles_df['ACT Reading Percentiles'][index]
        reading_percentile = ordinal(reading_percentile)

        index = percentiles_df.loc[percentiles_df['ACT Science'] == reading_score].index[0]
        science_percentile = percentiles_df['ACT Science Percentiles'][index]
        science_percentile = ordinal(science_percentile)

        # GET CATEGORY DATA
        questions = Question.objects.filter(exam=exam)

        subscores_category_data = {
            'CM':[0,0,0,None],
            'PSDA':[0,0,0,None],
            'HA':[0,0,0,None],
            'WC':[0,0,0,None],
            'EI':[0,0,0,None],
            'PAM':[0,0,0,None],
            'SEC':[0,0,0,None],
        }
        reading_science_category_data = {
            'D':[0,0,None],
            'I':[0,0,None],
            'S':[0,0,None],
            'GF':[0,0,None],
            'VC':[0,0,None],
            'F':[0,0,None],
            'NS':[0,0,None],
            'SS':[0,0,None],
            'H':[0,0,None],
            'DP':[0,0,None],
        }
        english_category_data = {
            'A':[0,0,None],
            'P':[0,0,None],
            'ST':[0,0,None],
            'VC':[0,0,None],
            'CW':[0,0,None],
            'ID':[0,0,None],
            'COMP':[0,0,None],
            'PS':[0,0,None],
            'R':[0,0,None],
            'TW':[0,0,None],
            'SP':[0,0,None],
            'RG':[0,0,None],
            'UP':[0,0,None],
            'TS':[0,0,None],
            'SX':[0,0,None],
        }
        math_category_data = {
            'FA':[0,0,None],
            'WP':[0,0,None],
            'VS':[0,0,None],
            'SE':[0,0,None],
            'Q':[0,0,None],
            'FOIL':[0,0,None],
            'AI':[0,0,None],
            'EXP':[0,0,None],
            'GEO':[0,0,None],
            'CR':[0,0,None],
            'TR':[0,0,None],
            '3D':[0,0,None],
            'PL':[0,0,None],
            'RAT':[0,0,None],
            'CN':[0,0,None],
            'TRIG':[0,0,None],
            'RG':[0,0,None],
            'PROB':[0,0,None],
            'STAT':[0,0,None],
            'LOG':[0,0,None],
            'RE':[0,0,None],
            'MISC':[0,0,None],
            'MMM':[0,0,None],
            'FN':[0,0,None],
        }

        category_data = {
            'CM':[0,0, None],
            'PSDA':[0,0,None],
            'HA':[0,0,None],
            'WC':[0,0,None],
            'EI':[0,0,None],
            'PAM':[0,0,None],
            'SEC':[0,0,None],
            'D':[0,0,None],
            'I':[0,0,None],
            'S':[0,0,None],
            'GF':[0,0,None],
            'VC':[0,0,None],
            'F':[0,0,None],
            'NS':[0,0,None],
            'SS':[0,0,None],
            'H':[0,0,None],
            'DP':[0,0,None],
            'A':[0,0,None],
            'P':[0,0,None],
            'ST':[0,0,None],
            'VC':[0,0,None],
            'CW':[0,0,None],
            'ID':[0,0,None],
            'COMP':[0,0,None],
            'PS':[0,0,None],
            'R':[0,0,None],
            'TW':[0,0,None],
            'SP':[0,0,None],
            'RG':[0,0,None],
            'UP':[0,0,None],
            'TS':[0,0,None],
            'SX':[0,0,None],
            'FA':[0,0,None],
            'WP':[0,0,None],
            'SE':[0,0,None],
            'Q':[0,0,None],
            'FOIL':[0,0,None],
            'AI':[0,0,None],
            'EXP':[0,0,None],
            'GEO':[0,0,None],
            'CR':[0,0,None],
            'TR':[0,0,None],
            '3D':[0,0,None],
            'PL':[0,0,None],
            'RAT':[0,0,None],
            'CN':[0,0,None],
            'TRIG':[0,0,None],
            'RG':[0,0,None],
            'PROB':[0,0,None],
            'STAT':[0,0,None],
            'LOG':[0,0,None],
            'RE':[0,0,None],
            'MISC':[0,0,None],
            'MMM':[0,0,None],
            'MC':[0,0,None],
            'FR':[0,0,None],
            'OI':[0,0,None],
        }

        for question in questions:
            category_string = question.categories
            categories = None
            try:
                categories = category_string.split(',')
            except:
                # this case occurs if there is only one category
                categories = [category_string]

            for category in categories:
                category = category.replace(' ', '')

                # handle the subscores category
                if category in subscores_category_data.keys():
                    # Increase the count of the category
                    subscores_category_data[category][0] += 1
                    # If answered correctly, increase the correct count of that category
                    selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                    if selected_answer.is_correct:
                        subscores_category_data[category][1] += 1

                if question.section.type == 'reading' or question.section.type == 'science':
                    if category in reading_science_category_data.keys():
                        # Increase the count of the category
                        reading_science_category_data[category][0] += 1
                        # If answered correctly, increase the correct count of that category
                        selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                        if selected_answer.is_correct:
                            reading_science_category_data[category][1] += 1
                elif question.section.type == 'english':
                    if category in english_category_data.keys():
                        # Increase the count of the category
                        english_category_data[category][0] += 1
                        # If answered correctly, increase the correct count of that category
                        selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                        if selected_answer.is_correct:
                            english_category_data[category][1] += 1
                elif question.section.type == 'math':
                    if category in math_category_data.keys():
                        # Increase the count of the category
                        math_category_data[category][0] += 1
                        # If answered correctly, increase the correct count of that category
                        selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                        if selected_answer.is_correct:
                            math_category_data[category][1] += 1

                if category not in category_data.keys():
                    print(category + ' is not in the category_data dictionary!!!')

        # Loop through the dictionary and perform the percentages computation
        for key in subscores_category_data:
            # NOTE: subscores are out of 15, so we have an additional value in the list
            # Assign 'NA' to categories with 0 appearances
            if subscores_category_data[key][0] == 0:
                subscores_category_data[key][3] = 'NA'
            else:
                # Assign the fraction in proportion to 15
                subscores_category_data[key][3] = int((subscores_category_data[key][1] * 15) / subscores_category_data[key][0])
                # Get percentage from the proportion to 15
                subscores_category_data[key][2] = int((subscores_category_data[key][3] / 15) * 100)

        for key in reading_science_category_data:
            # Assign 'NA' to categories with 0 appearances
            if reading_science_category_data[key][0] == 0:
                reading_science_category_data[key][2] = 'NA'
                # WE ARE SETTING THIS EQAUL TO 0 FOR NOW
                reading_science_category_data[key][2] = 0
            else:
                # Assign the percentage to the third element in the value list
                reading_science_category_data[key][2] = int((reading_science_category_data[key][1] / reading_science_category_data[key][0]) * 100)

        for key in english_category_data:
            # Assign 'NA' to categories with 0 appearances
            if english_category_data[key][0] == 0:
                english_category_data[key][2] = 'NA'
                # WE ARE SETTING THIS EQAUL TO 0 FOR NOW
                english_category_data[key][2] = 0
            else:
                # Assign the percentage to the third element in the value list
                english_category_data[key][2] = int((english_category_data[key][1] / english_category_data[key][0]) * 100)

        for key in math_category_data:
            # Assign 'NA' to categories with 0 appearances
            if math_category_data[key][0] == 0:
                math_category_data[key][2] = 'NA'
                # WE ARE SETTING THIS EQAUL TO 0 FOR NOW
                math_category_data[key][2] = 0
            else:
                # Assign the percentage to the third element in the value list
                math_category_data[key][2] = int((math_category_data[key][1] / math_category_data[key][0]) * 100)

        context = {
            'exam':exam,
            'user': user,
            'user_name': user_name,
            'current_date':current_date,
            'raw_english_score':raw_english_score,
            'raw_math_score':raw_math_score,
            'raw_reading_score':raw_reading_score,
            'raw_science_score':raw_science_score,
            'omitted_english':omitted_english,
            'omitted_math':omitted_math,
            'omitted_reading':omitted_reading,
            'omitted_science':omitted_science,
            'english_questions':english_questions,
            'math_questions':math_questions,
            'reading_questions':reading_questions,
            'science_questions':science_questions,
            'english_student_answers':english_student_answers,
            'math_student_answers':math_student_answers,
            'reading_student_answers':reading_student_answers,
            'science_student_answers':science_student_answers,
            'incorrect_english':incorrect_english,
            'incorrect_math':incorrect_math,
            'incorrect_reading':incorrect_reading,
            'incorrect_science':incorrect_science,
            'english_score':english_score,
            'math_score':math_score,
            'reading_score':reading_score,
            'science_score':science_score,
            'total_score':total_score,
            'english_questions_answers':english_questions_answers,
            'math_questions_answers':math_questions_answers,
            'reading_questions_answers':reading_questions_answers,
            'science_questions_answers':science_questions_answers,
            'percentile':percentile,
            'english_percentile':english_percentile,
            'math_percentile':math_percentile,
            'reading_percentile':reading_percentile,
            'science_percentile':science_percentile,
            'reading_science_category_data':reading_science_category_data,
            'english_category_data':english_category_data,
            'math_category_data':math_category_data,
        }

        return render(request, 'results/act-results.html', context)
    elif exam_type == 'DIAGNOSTIC':
        sat_raw_math_score = raw_math1_score + raw_math2_score

        incorrect_reading = 21 - (omitted_reading + raw_reading_score)
        incorrect_writing = 22 - (omitted_writing + raw_writing_score)
        incorrect_math1 = 10 - (omitted_math1 + raw_math1_score)
        incorrect_math2 = 15 - (omitted_math2 + raw_math2_score)
        incorrect_math = 30 - (omitted_math + raw_math_score)
        incorrect_english = 30 - (omitted_english + raw_english_score)
        incorrect_science = 21 - (omitted_science + raw_science_score)

        #SAT answers
        reading_questions_answers = zip(reading_questions, reading_student_answers)
        writing_questions_answers = zip(writing_questions, writing_student_answers)
        math1_questions_answers = zip(math1_questions, math1_student_answers)
        math2_questions_answers = zip(math2_questions, math2_student_answers)

        #ACT answers
        english_questions_answers = zip(english_questions, english_student_answers)
        math_questions_answers = zip(math_questions, math_student_answers)
        science_questions_answers = zip(science_questions, science_student_answers)

        # Get Percentiles
        module_dir = os.path.dirname(__file__) #get current directory
        percentiles_file_path = os.path.join(module_dir, 'data_files/Percentiles.csv')
        percentiles_df = pd.read_csv(percentiles_file_path)

        questions_correct_index = percentiles_df.loc[percentiles_df['Number of Questions Correct'] == sat_raw_math_score].index[0]
        sat_math_score = percentiles_df['Diagnostic SAT Math'][questions_correct_index]
        questions_correct_index = percentiles_df.loc[percentiles_df['Number of Questions Correct'] == raw_reading_score].index[0]
        sat_reading_score = percentiles_df['Diagnostic SAT Reading'][questions_correct_index] * 10
        questions_correct_index = percentiles_df.loc[percentiles_df['Number of Questions Correct'] == raw_writing_score].index[0]
        sat_writing_score = percentiles_df['Diagnostic SAT Writing'][questions_correct_index] * 10

        sat_reading_writing_score = sat_reading_score + sat_writing_score
        sat_total_score = sat_reading_writing_score + sat_math_score

        percentile_index = percentiles_df.loc[percentiles_df['SAT'] == sat_total_score].index[0]
        percentile = percentiles_df['SAT Percentiles'][percentile_index]
        raw_sat_percentile = percentile
        sat_percentile = ordinal(percentile)

        questions_correct_index = percentiles_df.loc[percentiles_df['Number of Questions Correct'] == raw_math_score].index[0]
        act_math_score = percentiles_df['Diagnostic ACT Math'][questions_correct_index]
        questions_correct_index = percentiles_df.loc[percentiles_df['Number of Questions Correct'] == raw_english_score].index[0]
        act_english_score = percentiles_df['Diagnostic ACT English'][questions_correct_index]
        questions_correct_index = percentiles_df.loc[percentiles_df['Number of Questions Correct'] == raw_science_score].index[0]
        act_science_score = percentiles_df['Diagnostic ACT Science'][questions_correct_index]

        act_total_score = (act_math_score + act_english_score + act_science_score) // 3

        percentile_index = percentiles_df.loc[percentiles_df['ACT'] == act_total_score].index[0]
        percentile = percentiles_df['ACT Percentiles'][percentile_index]
        raw_act_percentile = percentile
        act_percentile = ordinal(percentile)

        # GET CATEGORY DATA
        questions = Question.objects.filter(exam=exam)

        subscores_category_data = {
            'CM':[0,0,0,None],
            'PSDA':[0,0,0,None],
            'HA':[0,0,0,None],
            'WC':[0,0,0,None],
            'EI':[0,0,0,None],
            'PAM':[0,0,0,None],
            'SEC':[0,0,0,None],
        }
        reading_science_category_data = {
            'D':[0,0,None],
            'I':[0,0,None],
            'S':[0,0,None],
            'GF':[0,0,None],
            'VC':[0,0,None],
            'F':[0,0,None],
            'NS':[0,0,None],
            'SS':[0,0,None],
            'H':[0,0,None],
            'DP':[0,0,None],
        }
        english_category_data = {
            'A':[0,0,None],
            'P':[0,0,None],
            'ST':[0,0,None],
            'VC':[0,0,None],
            'CW':[0,0,None],
            'ID':[0,0,None],
            'COMP':[0,0,None],
            'PS':[0,0,None],
            'R':[0,0,None],
            'TW':[0,0,None],
            'SP':[0,0,None],
            'RG':[0,0,None],
            'UP':[0,0,None],
            'TS':[0,0,None],
            'SX':[0,0,None],
        }
        math_category_data = {
            'FA':[0,0,None],
            'WP':[0,0,None],
            'VS':[0,0,None],
            'SE':[0,0,None],
            'Q':[0,0,None],
            'FOIL':[0,0,None],
            'AI':[0,0,None],
            'EXP':[0,0,None],
            'GEO':[0,0,None],
            'CR':[0,0,None],
            'TR':[0,0,None],
            '3D':[0,0,None],
            'PL':[0,0,None],
            'RAT':[0,0,None],
            'CN':[0,0,None],
            'TRIG':[0,0,None],
            'RG':[0,0,None],
            'PROB':[0,0,None],
            'STAT':[0,0,None],
            'LOG':[0,0,None],
            'RE':[0,0,None],
            'MISC':[0,0,None],
            'MMM':[0,0,None],
            'FN':[0,0,None],
        }

        category_data = {
            'CM':[0,0, None],
            'PSDA':[0,0,None],
            'HA':[0,0,None],
            'WC':[0,0,None],
            'EI':[0,0,None],
            'PAM':[0,0,None],
            'SEC':[0,0,None],
            'D':[0,0,None],
            'I':[0,0,None],
            'S':[0,0,None],
            'GF':[0,0,None],
            'VC':[0,0,None],
            'F':[0,0,None],
            'NS':[0,0,None],
            'SS':[0,0,None],
            'H':[0,0,None],
            'DP':[0,0,None],
            'A':[0,0,None],
            'P':[0,0,None],
            'ST':[0,0,None],
            'VC':[0,0,None],
            'CW':[0,0,None],
            'ID':[0,0,None],
            'COMP':[0,0,None],
            'PS':[0,0,None],
            'R':[0,0,None],
            'TW':[0,0,None],
            'SP':[0,0,None],
            'RG':[0,0,None],
            'UP':[0,0,None],
            'TS':[0,0,None],
            'SX':[0,0,None],
            'FA':[0,0,None],
            'WP':[0,0,None],
            'SE':[0,0,None],
            'Q':[0,0,None],
            'FOIL':[0,0,None],
            'AI':[0,0,None],
            'EXP':[0,0,None],
            'GEO':[0,0,None],
            'CR':[0,0,None],
            'TR':[0,0,None],
            '3D':[0,0,None],
            'PL':[0,0,None],
            'RAT':[0,0,None],
            'CN':[0,0,None],
            'TRIG':[0,0,None],
            'RG':[0,0,None],
            'PROB':[0,0,None],
            'STAT':[0,0,None],
            'LOG':[0,0,None],
            'RE':[0,0,None],
            'MISC':[0,0,None],
            'MMM':[0,0,None],
            'MC':[0,0,None],
            'FR':[0,0,None],
            'OI':[0,0,None],
        }

        for question in questions:
            category_string = question.categories
            categories = None
            try:
                categories = category_string.split(',')
            except:
                # this case occurs if there is only one category
                categories = [category_string]

            for category in categories:

                category = category.replace(' ', '')

                # handle the subscores category
                if category in subscores_category_data.keys():
                    # Increase the count of the category
                    subscores_category_data[category][0] += 1
                    # If answered correctly, increase the correct count of that category
                    selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                    if selected_answer.is_correct:
                        subscores_category_data[category][1] += 1

                if question.section.type == 'reading' or question.section.type == 'science':
                    if category in reading_science_category_data.keys():
                        # Increase the count of the category
                        reading_science_category_data[category][0] += 1
                        # If answered correctly, increase the correct count of that category
                        selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                        if selected_answer.is_correct:
                            reading_science_category_data[category][1] += 1
                elif question.section.type == 'english' or question.section.type == 'writing':
                    if category in english_category_data.keys():
                        # Increase the count of the category
                        english_category_data[category][0] += 1
                        # If answered correctly, increase the correct count of that category
                        selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                        if selected_answer.is_correct:
                            english_category_data[category][1] += 1
                elif question.section.type == 'math' or question.section.type == 'math1' or question.section.type == 'math2':
                    if category in math_category_data.keys():
                        # Increase the count of the category
                        math_category_data[category][0] += 1
                        # If answered correctly, increase the correct count of that category
                        selected_answer = Student_Answer.objects.filter(user=user, exam=exam, question=question)[0]
                        if selected_answer.is_correct:
                            math_category_data[category][1] += 1

                if category not in category_data.keys():
                    print(category + ' is not in the category_data dictionary!!!')

        # Loop through the dictionary and perform the percentages computation
        for key in subscores_category_data:
            # NOTE: subscores are out of 15, so we have an additional value in the list
            # Assign 'NA' to categories with 0 appearances
            if subscores_category_data[key][0] == 0:
                subscores_category_data[key][3] = 'NA'
            else:
                # Assign the fraction in proportion to 15
                subscores_category_data[key][3] = int((subscores_category_data[key][1] * 15) / subscores_category_data[key][0])
                # Get percentage from the proportion to 15
                subscores_category_data[key][2] = int((subscores_category_data[key][3] / 15) * 100)

        for key in reading_science_category_data:
            # Assign 'NA' to categories with 0 appearances
            if reading_science_category_data[key][0] == 0:
                reading_science_category_data[key][2] = 'NA'
                # WE ARE SETTING THIS EQAUL TO 0 FOR NOW
                reading_science_category_data[key][2] = 0
            else:
                # Assign the percentage to the third element in the value list
                reading_science_category_data[key][2] = int((reading_science_category_data[key][1] / reading_science_category_data[key][0]) * 100)

        for key in english_category_data:
            # Assign 'NA' to categories with 0 appearances
            if english_category_data[key][0] == 0:
                english_category_data[key][2] = 'NA'
                # WE ARE SETTING THIS EQAUL TO 0 FOR NOW
                english_category_data[key][2] = 0
            else:
                # Assign the percentage to the third element in the value list
                english_category_data[key][2] = int((english_category_data[key][1] / english_category_data[key][0]) * 100)

        for key in math_category_data:
            # Assign 'NA' to categories with 0 appearances
            if math_category_data[key][0] == 0:
                math_category_data[key][2] = 'NA'
                # WE ARE SETTING THIS EQAUL TO 0 FOR NOW
                math_category_data[key][2] = 0
            else:
                # Assign the percentage to the third element in the value list
                math_category_data[key][2] = int((math_category_data[key][1] / math_category_data[key][0]) * 100)

        context = {
            'exam':exam,
            'user': user,
            'user_name':user_name,
            'current_date':current_date,
            'sat_reading_score':math.trunc(sat_reading_score),
            'raw_reading_score':raw_reading_score,
            'omitted_reading':omitted_reading,
            'sat_writing_score':math.trunc(sat_writing_score),
            'raw_writing_score':raw_writing_score,
            'omitted_writing':omitted_writing,
            'sat_math_score':math.trunc(sat_math_score),
            'raw_math1_score':raw_math1_score,
            'omitted_math1':omitted_math1,
            'raw_math2_score':raw_math2_score,
            'omitted_math2':omitted_math2,
            'raw_math_score':raw_math_score,
            'omitted_math':omitted_math,
            'act_english_score':math.trunc(act_english_score),
            'raw_english_score':raw_english_score,
            'omitted_english':omitted_english,
            'act_science_score':math.trunc(act_science_score),
            'raw_science_score':raw_science_score,
            'omitted_science':omitted_science,
            'act_math_score':math.trunc(act_math_score),
            'sat_total_score':math.trunc(sat_total_score),
            'act_total_score':math.trunc(act_total_score),
            'sat_percentile':sat_percentile,
            'act_percentile':act_percentile,
            'raw_act_percentile':raw_act_percentile,
            'raw_sat_percentile':raw_sat_percentile,
            'reading_questions_answers':reading_questions_answers,
            'writing_questions_answers':writing_questions_answers,
            'math1_questions_answers':math1_questions_answers,
            'math2_questions_answers':math2_questions_answers,
            'test_questions_answers':reading_questions_answers,
            'english_questions_answers':english_questions_answers,
            'math_questions_answers':math_questions_answers,
            'science_questions_answers':science_questions_answers,
            'reading_science_category_data':reading_science_category_data,
            'english_category_data':english_category_data,
            'math_category_data':math_category_data,
            'incorrect_math':incorrect_math,
            'incorrect_math1':incorrect_math1,
            'incorrect_math2':incorrect_math2,
            'incorrect_english':incorrect_english,
            'incorrect_reading':incorrect_reading,
            'incorrect_science':incorrect_science,
            'incorrect_writing':incorrect_writing,

        }
        return render(request, 'results/diagnostic-score-report.html', context)
