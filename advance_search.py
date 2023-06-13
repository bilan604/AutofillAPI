import re
import os
import time
import base64
import requests
import json
from bs4 import BeautifulSoup
import openai


def getMultiPrompt(text, src, url=""):
    if url:
        multi_prompt = f'This is the html content from {url}:\n”””\n{src}\n”””\n\n'
    else:
        multi_prompt = f'Here is the html content from a element in a webpage:\n”””\n{src}\n”””\n\n'
    
    multi_prompt += f'The text rendered onto the webpage from the content is:\n“””\n{text}\n“””\n\n'
    multi_prompt += f'You must determine whether the text contains at least one user-input-question. A user-input-question MUST contain two things:\n'
    multi_prompt += f'1. The HTML content must contain the text for the question(s), or a text label for the question(s) such as a <span> tag.\n'
    multi_prompt += f'2. The HTML content must contain the tag for user input corresponding to the question, such as an <input> tag.\n\n'
    multi_prompt += f'Some examples of questions are “First Name”, “Carrier Booking Ref*”, “Color”, “License No”, and “Name*”. If there is no user-input-question or if the user-input-question does not meet BOTH requirements, respond with either “FALSE:NO QUESTION” or “FALSE:INCOMPLETE QUESTION”.'
    multi_prompt += f'Otherwise, respond with “TRUE:” followed immediately by a JSON object containing the user-input-questions. The keys for each user-input-question will be “question”, “question_identifier”, and “answer_identifier”. The identifiers are the opening tag for the question(s) and answer(s).'
    multi_prompt += \
"""i.e.: TRUE:[{\
“question”: “Email Address*”,\
“question_identifier”: “<span class="M7eMe">Email Address*</span>”,\
“answer_identifier”: “<input type="text" class="whsOnd zHQkBf" jsname="YPqjbf" autocomplete="off" tabindex="0" aria-labelledby="i1" aria-describedby="i2 i3" dir="auto" data-initial-dir="auto" data-initial-value="">”\
},\
{\
“question”: “Prod. Date”,\
“question_identifier”: “<span style="white-space:pre-wrap">Prod. Date</span>”,\
“answer_identifier”: “<input type="text" class="whsOnd zHQkBf" jsname="YPqjbf" autocomplete="off" tabindex="0" aria-labelledby="i101" aria-describedby="i102 i103" dir="auto" data-initial-dir="auto" data-initial-value="">”\
}]"""
    return multi_prompt


##
def getTags(htmlContent):
    if htmlContent.find("<body") != 0:
        soup = BeautifulSoup(htmlContent, "html.parser")
        htmlContent = str(soup.find_all("body")[0])
        
    soup = BeautifulSoup(htmlContent, "html.parser")
    tags = soup.find_all()
    tags = list(map(str, tags))
    return tags


def getWords(s):
    words = re.sub("</.+?>", "<[/element]>", s)
    words = re.sub("<.+?>", "<[element]>", words)
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = " ".join([w.strip() for w in words.split(" ") if w.strip()])
    words = words.strip()
    return words



def askOpenAI003(api_key, query):
    if not api_key:
        print("Not implemented checking yet")
    if type(query) != str:
        print("Query was not string")
        return None
    if len(query) == 0:
        return None
    # Check if a command got passed in
    elif len(query) >= 1 and query[0] == "/":
        print("askOpenAI003(): command passed in as query")
        return None

    try:
        message = ""
        response = openai.Completion.create(model="text-davinci-003",
                                            prompt=query,
                                            temperature=0.25,
                                            max_tokens=4095)

        message = response.choices[0].text.strip()
        return message
    except Exception as e:
        print("Error on OpenAI API Call:", e)
        return None


def contains_duplicate_questions(src):
    src = re.sub("{.+?}", "", src)
    src = re.sub("<.+?>", "^^^^", src)
    src = re.sub("\n", " ", src)
    src = re.sub(" +", " ", src)
    src = re.sub("[\^\^\^\^ | \^\^\^\^| \^\^\^\^ ]", "^^^^", src)
    src = re.sub("(\^\^\^\^)+", "^^^^", src)
    lst = [s.strip() for s in src.split("^^^^") if s.strip()]
    dd = {}
    for s in lst:
        if s not in dd:
            dd[s] = 1
        else:
            dd[s] = 1
    verdict = False
    for key in dd:
        if dd[key] > 1 and s == re.sub("\^", "", s):
            print("duplicate key:", key)
            verdict = True    
    return verdict


def parseLstOfJsonStrs(s):
    jsons = []
    curr = ""
    add = False
    for letter in s:
        if letter == "{":
            add = True
        elif letter == "}":
            add = False
            curr += letter
            jsons.append(curr)
            curr = ""
        else:
            if add:
                curr += letter
            else:
                pass
    return jsons


def question_answer_llm(id, bodyContent):
    l,r = bodyContent.find("<body"), bodyContent.find("</body>")
    bodyContent = bodyContent[l:r+len("</body>")]
    
    responses = []

    stack = [bodyContent]
    while stack:
        newStack = []
        for item in stack:
            words = getWords(item).strip()
            text = re.sub("<.+?>", "", words).strip()
            if len(item) + len(text) < 10000:
                tags = list(map(str, BeautifulSoup(item, 'html.parser').find_all()))
                newStack += tags
            # different context same question appears
            elif contains_duplicate_questions(item):
                print("duplicate item with length: ", len(item))
                tags = list(map(str, BeautifulSoup(item, 'html.parser').find_all()))
                newStack += tags
            else:
                # do llm
                query_prompt = getMultiPrompt(text, item)
                print("------------query_prompt:")
                print(query_prompt)
                
                response = askOpenAI003(id, query_prompt)
                print("----------GPT3 response:")
                print(response)
                print("\n")
                if response.find("TRUE:") == 0:
                    user_input_questions = parseLstOfJsonStrs(response[4:])
                    print(f"{user_input_questions=}\n")
                    responses += user_input_questions

        if not newStack:
            return responses
        stack = newStack
    print("responses:", responses)
    responses = list(map(json.loads, responses))
    return responses








