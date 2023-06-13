import os
import json
import openai
from target import question_answer_fast
from answering import answer_input_questions
from advance_search import question_answer_llm
from container.src.validation import load_credentials
from flask import Flask, redirect, render_template, request, url_for


count = 0
app = Flask(__name__)


@app.route("/inputQuestions/", methods=("GET", "POST"))
def inputQuestionsAPI():
    data = request.json
    if request.method == "POST":
        # 
        id = ""
        if "id" in data:
            id = data["id"]
        
        # Find the operation requested
        operation = ""
        if "operation" in data:
            operation = data["operation"]

        # Parses the pages innerHTML and finds the questions and answer input elements
        # Uses LLM prompting
        if operation == "Question-Answer-LLM":
            htmlContent = data["html_content"]
            qas = question_answer_llm(id, htmlContent)
            return json.dumps({"response": qas})
        
        # Parses the pages innerHTML and finds the questions and answer input elements
        # Uses same parent element to find question answer pairs, must faster
        if operation == "Question-Answer-Fast":
            htmlContent = data["html_content"]
            qas = question_answer_fast(id, htmlContent)
            return json.dumps({"response": qas})
        
        # Answers questions given and id for an account with stored information
        if operation == "Answer-Input-Questions":
            qas = data["qas"]
            answers = answer_input_questions(id, qas)
            return json.dumps({"response": answers})
    
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

    return "Hello, World!"




if __name__ == "__main__":
    path = "c:/Users/bill/github/AutofillAPI"
    os.chdir(path)
    credentials = load_credentials()
    id = credentials["OPENAI_API_KEY"]
    openai.api_key = id
    
    app.run()