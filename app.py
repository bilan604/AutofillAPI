import os
import openai
import json
import flask
from target import getInputQuestions, filterAnswerStoredQuestions
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
        if operation == "Question-Answer-Fast":
            htmlContent = data["html_content"]
            qas = getInputQuestions(id, htmlContent)
            answers = filterAnswerStoredQuestions(id, qas)
            return answers
        elif operation == "Identify-Question-Answers":
            htmlContent = data["html_content"]
            qas = getInputQuestions(id, htmlContent)
            return qas
        elif operation == "Answer-Input-Questions":
            qas = data["qas"]
            answers = filterAnswerStoredQuestions(id, qas)
            return answers
    
    return "Hello world, InputQuestions!"


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
        
        # Do the operation
        if operation == "Question-Answer-Fast":
            htmlContent = data["html_content"]
            qas = getInputQuestions(id, htmlContent)
            answers = filterAnswerStoredQuestions(id, qas)
            return answers

    return "Hello, World!"


def load_credentials(path):
    os.chdir(path)
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
    credentials = load_credentials(path)
    openai.api_key = credentials["OPENAI_API_KEY"]
    app.run()