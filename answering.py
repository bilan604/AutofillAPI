import re
from container.answer_loading import load_question_data

#
def parseTextSpacing(s):
    words = re.sub("</.+?>", "<[/element]>", s)
    words = re.sub("<.+?>", "<[element]>", words)
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = " ".join([w.strip() for w in words.split(" ") if w.strip()])
    words = words.strip()
    return words

# Answering related functions below
def getAnsweredQuestions(temp):
    dd = {}
    for key in temp:
        if "/" not in key:
            key = parseTextSpacing(key)
            dd[key] = temp[key]
        else:
            for keyItem in key.split("/"):
                keyItem = parseTextSpacing(keyItem)
                dd[keyItem] = temp[key]
    return dd


def checkAnsweredQuestions(pageQuestion, answeredQuestions):
        for answeredQuestion in answeredQuestions:
            if answeredQuestion.find(pageQuestion) == 0:
                # and/or other specifications
                return answeredQuestion
        return None


def answer_input_questions(id, inputQuestions):
    ###########
    # This is an override 
    #questionData = load_question_data(id)
    questionData = {"id": "testId", "storedResponses": {"name": "John Doe", "first name": "John", "last name": "Doe", "full legal name/full name/name": "John Doe", "email/email address": "john-doe-123@gmail.com", "phone/phone number/mobile number": "1234567890", "address/home address/address line 1": "123 Test s.t.", "state": "California", "country": "United States", "date of birth/D.O.B.": "01/01/1990", "LinkedIn/LinkedIn URL": "https://www.linkedin.com/in/bill-lan-6aaa01147/", "Github/Github URL/Github Link/Portfolio URL/Portfolio Link": "https://github.com/bilan604"}}
    ###########

    if not questionData:
        return {"response": "No information found for id " + id}
    
    #print("inputQuestions", inputQuestions)
    temp = questionData["storedResponses"]
    answeredQuestions = getAnsweredQuestions(temp)
    #print("answeredQuestions", answeredQuestions)
    matchedQuestions = []
    for inputQuestion in inputQuestions:

        pageQuestion = inputQuestion["question"]
        pageQuestion = re.sub("[^a-zA-Z| ]", "", pageQuestion)
        pageQuestion = re.sub(" +?", " ", pageQuestion)
        pageQuestion = pageQuestion.lower().strip()
        if pageQuestion in answeredQuestions:
            matchedQA = inputQuestion.copy()
            matchedQA["answer"] = answeredQuestions[pageQuestion]
            matchedQuestions.append(matchedQA)
        else:
            relevantQuestion = checkAnsweredQuestions(pageQuestion, answeredQuestions)
            if not relevantQuestion: continue
            matchedQA = inputQuestion.copy()
            matchedQA["answer"] = answeredQuestions[relevantQuestion]
            matchedQuestions.append(matchedQA)
    #print("matchedQuestions:", matchedQuestions, "\n")
    return {"response": matchedQuestions}