import os
import json
import openai
from target import question_answer_fast
from answering import answer_input_questions
from advance_search import question_answer_prompts, question_answer_prompting
from container.src.validation import load_credentials
from flask import Flask, redirect, render_template, request, url_for


count = 0
app = Flask(__name__)


@app.route("/inputQuestions/", methods=("GET", "POST"))
def inputQuestionsAPI():
    if type(request.json) == str:
        try:
            data = json.loads(request.json)
        except:
            print("Invalid request parameter provided. Please use json object")
    else:
        data = request.json
    
    print("Data recieved with fields:", list(data.keys()))
    # ToDo: Refactor this so it finds the function from a map instead of with if statements
    if request.method == "POST":
        # Not using .get method to keep dataType consistent
        id = ""
        if "id" in data:
            id = data["id"]
        
        # Specifies a functionality for the request
        operation = ""
        if "operation" in data:
            operation = data["operation"]

        # Parses the pages innerHTML and finds the questions and answer input elements
        # Uses LLM prompting
        if operation == "Question-Answer-LLM":
            # This functionality is the following two operations combined
            htmlContent = data["requestData"]
            prompts = question_answer_prompts(id, htmlContent)
            responses = question_answer_prompting(id, prompts)
            return json.dumps(qas)
        
        if operation == "Question-Answer-Prompts":
            # "Question-Answer-LLM" but only returns the prompts
            htmlContent = data["requestData"]
            prompts = question_answer_prompts(id, htmlContent)
            return json.dumps(prompts)
        
        if operation == "Question-Answer-Prompting":
            # "Question-Answer-LLM" but only returns the prompts
            prompts = data["requestData"]
            responses = question_answer_prompting(id, prompts)
            return json.dumps(responses)
        
        # Parses the pages innerHTML and finds the questions and answer input elements
        # Uses same parent element to find question answer pairs, must faster
        if operation == "Question-Answer-Fast":
            htmlContent = data["requestData"]
            qas = question_answer_fast(id, htmlContent)
            return json.dumps(qas)
        
        if operation == "Question-Answer-Fast-2":
            # Gets the question tag and superset question tags
            # Name, NameYour Answer are both returned
            htmlContent = data["requestData"]
            qas = question_answer_fast(id, htmlContent,False)
            return json.dumps(qas)
        
        # Answers questions given and id for an account with stored information
        if operation == "Answer-Input-Questions":
            qas = data["requestData"]
            answers = answer_input_questions(id, qas)
            return json.dumps(answers)
        
        if operation == "Add-User-QAs":
            # "Question-Answer-LLM" but only returns the prompts
            prompts = data["requestData"]
            responses = question_answer_prompting(id, prompts)
            return json.dumps(responses)
    
    return json.dumps([None])


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
    ##
    path = "c:/Users/bill/github/AutofillAPI"
    os.chdir(path)
    ##
    credentials = load_credentials()
    id = credentials["OPENAI_API_KEY"]
    openai.api_key = id
    app.run()

