import os
import openai
import json
import flask
from app import get_llm_input_questions
from flask import Flask, redirect, render_template, request, url_for


count = 0
app = Flask(__name__)


@app.route("/inputQuestions/", methods=("GET", "POST"))
def inputQuestionsAPI():
    data = request.json
    if request.method == "POST":
        id = ""
        if "id" in data:
            id = data["id"]
        
        # Find the operation requested
        operation = ""
        if "operation" in data:
            operation = data["operation"]
        
        # Do the operation
        if operation == "Question-Answer-Identification":
            htmlContent = data["html_content"]
            inputQuestions = get_llm_input_questions(id, htmlContent)
            print(f"{inputQuestions=}\n")
            return inputQuestions
        
        """
        elif operation == "Question-Answer-Fast":
            htmlContent = data["html_content"]
            qas = getFastQA(id, htmlContent)
            answers = answerQAs(id, qas)
            return answers
        elif operation == "Identify-Question-Answers":
            htmlContent = data["html_content"]
            qas = getFastQA(id, htmlContent)
            return qas
        elif operation == "Answer-Input-Questions":
            qas = data["qas"]
            answers = answerQAs(id, qas)
            return answers
        return {"response": "401"}
        """
    return None


@app.route("/", methods=("GET", "POST"))
def index():
    data = request.json
    if request.method == "POST":
        id = ""
        if "id" in data:
            id = data["id"]
        # Find the operation requested
        operation = ""
        if "operation" in data:
            operation = data["operation"]
        return {"response": "Hello, World!"}
        """
        # Do the operation
        if operation == "Question-Answer":
            htmlContent = data["html_content"]
            answers = getQA(id, htmlContent)
            return answers
        
        elif operation == "Question-Answer-Fast":
            htmlContent = data["html_content"]
            qas = getFastQA(id, htmlContent)
            for item in qas:
                for key, val in item.items():
                    print(key, val)
            answers = answerQAs(id, qas)
            return answers
        elif operation == "Google-Search":
            return {"response": "Not added yet"}
        """
    return "placeholder webpage no longer supported"
    #result = request.args.get("result")
    #return render_template("index.html", result=result)


def load_credentials():
    rightPath = False
    for file in os.listdir():
        if file == '.env':
            rightPath = True
            break
    if not rightPath:
        print("Please check path: .env file not in current working directory.")
        return {}
    
    credentials = {}
    with open('.env', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if not line: continue
            lineLst = line.split("=")
            KEY = lineLst[0]
            VALUE = "".join(lineLst[1:])
            credentials[KEY] = VALUE
    return credentials


if __name__ == "__main__":
    path = "c:/Users/bill/github/AutofillAPI"
    os.chdir(path)
    credentials = load_credentials()
    openai.api_key = credentials["ALEX_OPENAI_API_KEY"]
    app.run()