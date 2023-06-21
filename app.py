import os
import json
import openai
from dotenv import load_dotenv
from functionHandling import *
from flask import Flask, redirect, render_template, request, url_for
load_dotenv()


count = 0
app = Flask(__name__)

operationFunctionsMap = {
    "Question-Answer-LLM": doQuestionAnswerLLM,
    "Question-Answer-Prompts": doQuestionAnswerPrompts,
    "Question-Answer-Prompting": doQuestionAnswerPrompting,
    "Question-Answer-Fast": doQuestionAnswerFast,
    "Question-Answer-Fast-2": doQuestionAnswerFast2,
    "Answer-Input-Questions": doAnswerInputQuestions
}


def operationFunctionHandler(requestorId, data):
    operation = data.get("operation", "")
    
    if operation not in operationFunctionsMap:
        return "Invalid operation"
    
    return operationFunctionsMap[operation](requestorId, data)


@app.route("/inputQuestions/", methods=("GET", "POST"))
def inputQuestionsAPI():
    print("Function call, inputQuestionsAPI()")
    if type(request.json) != str:
        data = request.json
    else:
        try:
            data = json.loads(request.json)
        except:
            print("Invalid request data recieved at inputQuestionsAPI()")
            return "Invalid request data."
    
    if request.method == "POST":
        # an id for loading saved questions and answers
        requestorId = data.get("id", "") 
        return operationFunctionHandler(requestorId, data)
    
    return json.dumps([None])


@app.route("/", methods=("GET", "POST"))
def index():
    data = request.json
    if request.method == "POST":
        return "POST Hello, World!"
    return "GET Hello World!"


if __name__ == "__main__":
    print(os.getcwd())
    path = "c:/Users/bill/github/AutofillAPI"
    os.chdir(path)

    KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = KEY
    app.run()

