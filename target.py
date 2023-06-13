import re
from bs4 import BeautifulSoup


def getTags(htmlContent):
    soup = BeautifulSoup(htmlContent, "html.parser")
    tags = soup.find_all()
    tags = list(map(str, tags))
    return tags


def parseTextSpacing(s):
    words = re.sub("</.+?>", "<[/element]>", s)
    words = re.sub("<.+?>", "<[element]>", words)
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = " ".join([w.strip() for w in words.split(" ") if w.strip()])
    words = words.strip()
    return words


def addAnswersToDD(dd, tags):
    qas = []
    for key, val in dd.items():
        parentTag = None
        for tag in tags:
            if val[1] in tag and "<input" in tag:
                if not parentTag or len(parentTag) >= len(tag):
                    parentTag = tag
        inputs = BeautifulSoup(parentTag, 'html.parser').find_all('input')
        inputs = list(map(str, inputs))
        dd[key].append(inputs[0])
        # inputs of length 1 constraint:
        # Returns input forms with only one element for answering (No multi-select)
        if len(inputs) == 1:
            qas.append({
            "question": dd[key][0],
            "question_identifier": dd[key][1],
            "answer_identifier": dd[key][2]
            })
    return qas


def checkAnsweredQuestions(pageQuestion, answeredQuestions):
        for answeredQuestion in answeredQuestions:
            if answeredQuestion.find(pageQuestion) == 0:
                # and/or other specifications
                return answeredQuestion
        return None


def getInputQuestions(id, bodyContent):
    tags = getTags(bodyContent)
    questions = {}
    for i, tag in enumerate(tags):
        if len(tag) > 100000: continue
        
        words = parseTextSpacing(tag)
        if 1 <= len(words) < 20:
            if words not in questions:
                questions[words] = [tag, i]
            else:
                if len(questions[words][0]) > len(tag):
                    questions[words] = [tag, i]
    
    # A {i (index of tag from tags): [question: str, tag_identifier (for question): str]}
    dd = {}
    for question, questionHTML in questions.items():
        dd[questionHTML[1]] = [question, questionHTML[0]]

    qas = addAnswersToDD(dd, tags) 
    return qas


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


def filterAnswerStoredQuestions(id, inputQuestions):
    ###########
    # This is an override
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