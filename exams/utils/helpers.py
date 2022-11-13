from questions.models import Question

def getMaterialUrlFromQuestion(question: Question):
    passageNum = question.passage
    section = question.section
    currNum = question.question_number
    currQuestion = question
    while currQuestion.passage == passageNum and currNum > 0:
        currQuestion = Question.objects.get(question_number = currNum, section = section)
        if currQuestion.material:
            return currQuestion.material.url
        currNum -= 1
    
    print("No material found for this question")
    return None