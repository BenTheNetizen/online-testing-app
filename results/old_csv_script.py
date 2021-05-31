def file_upload(request):
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        csv_file = request.FILES['file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a csv file')

        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        #processing variables
        exam_name = ''
        current_section = ''
        question_number = 1

        #Declare object variables to reduce querying to database
        exam_object = None
        section_object = None
        question_object = None

        #import pdb; pdb.set_trace()
        for column in csv.reader(io_string, delimiter=',', quotechar="|", skipinitialspace=True):
            print(column)
            #create new exam
            if question_object is None:
                exam_name = column[0]
                exam_object, created = Exam.objects.get_or_create(
                    name = exam_name
                )

            #if we have a new section, then we create a new section
            if current_section != column[1]:
                current_section = column[1]
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
            question_object, created = Question.objects.get_or_create(
                question_number = question_number,
                text = column[2],
                section = section_object,
            )
            question_number += 1

            answer_object_A, created = Answer.objects.get_or_create(
                text = column[3],
                letter = 'A',
                question = question_object
            )

            answer_object_B, created = Answer.objects.get_or_create(
                text = column[4],
                letter = 'B',
                question = question_object
            )

            answer_object_C, created = Answer.objects.get_or_create(
                text = column[5],
                letter = 'C',
                question = question_object
            )

            answer_object_D, created = Answer.objects.get_or_create(
                text = column[6],
                letter = 'D',
                question = question_object
            )

    return render(request, 'exams/file_upload.html')
