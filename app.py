import os
import openai
import json
import flask
from flask import Flask, redirect, render_template, request, url_for
from functions import *

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
        if not id or not operation:
            return "Please specify id and operation"
        # Do the operation
        if operation == "Question-Answer-Identification":
            htmlContent = data["html_content"]
            inputQuestions = get_llm_input_questions(id, htmlContent)
            return inputQuestions
    return "Hello World, inputQuestions!"


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
    return "Hello, World!"


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
    openai.api_key = credentials["OPENAI_API_KEY"]
    app.run()