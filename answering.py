import re
import json
from container.answer_loading import load_question_data


def parseAnswerTextSpacing(s):
    # Lowercase version
    words = re.sub("-", " ", s.lower().strip())
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = " ".join([w.strip() for w in words.split(" ") if w.strip()])
    words = words.strip()
    return words


def checkAnsweredQuestions(pageQuestion, answeredQuestions):
        for answeredQuestion in answeredQuestions:
            if answeredQuestion.find(pageQuestion) == 0:
                # and/or other specifications
                return answeredQuestion
        return None


#### placeholder for data retrieval/recieving endpoint
def load_question_data_plc(id):
    import numpy as np
    import pandas as pd
    questionData = {}
    df = pd.read_csv("data/bilan604.txt")
    mtx = np.array(df)
    for i in range(len(mtx)):
        row = [ij for ij in list(mtx[i,:]) if str(ij).lower() != "nan"]
        questionData[row[0]] = []
        for j in range(1, len(row)):
            questionData[row[0]] += [row[j]]
    return questionData


def answer_input_questions(id, inputQuestions):
    
    ###########
    # OVERRIDE
    questionData = load_question_data_plc(id)
    ##########

    if not questionData:
        return "No information found for id " + id

    def getAnsweredQuestions(questionData):
        # points to the input question to retrieve it
        pointer = {}
        for answer, question_synonyms in questionData.items():
            for question in question_synonyms:
                # parse the spacing for pointers to the answer, i.e. "full name"
                question = parseAnswerTextSpacing(question)
                pointer[question] = answer
        return pointer

    # Helper func to make retriever
    answeredQuestions = getAnsweredQuestions(questionData)
    matchedQuestions = []
    for inputQuestion in inputQuestions:
        # ToDo: add webpag support for questions formatted as synonym1/synonym2
        pageQuestion = inputQuestion["question"]
        pageQuestion = parseAnswerTextSpacing(pageQuestion)
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
    return matchedQuestions