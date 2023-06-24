import re
import json
import openai
import requests
import tiktoken
from container.parsing import load_response
from bs4 import BeautifulSoup
from container.parsing import getWords


def getMultiPrompt(text, src, url=""):
    if url:
        multi_prompt = f'This is the html content from {url}:\n”””\n{src}\n”””\n\n'
    else:
        multi_prompt = f'Here is the html content from a element in a webpage:\n”””\n{src}\n”””\n\n'
    
    multi_prompt += f'The text rendered onto the webpage from the content is:\n“””\n{text}\n“””\n\n'
    multi_prompt += f'You must determine whether the text contains at least one user-input-question. A user-input-question MUST contain two things:\n'
    multi_prompt += f'1. The HTML content must contain the text for the label/question(s), or a text label for the question(s) such as a <span> tag.\n'
    multi_prompt += f'2. The HTML content must contain the tag for user input corresponding to the question, such as an <input> tag.\n\n'
    multi_prompt += f'Some examples of questions are “First Name”, “Carrier Booking Ref*”, “Color”, “License No”, and “Name*”. If there is no user-input-question or if the user-input-question does not meet BOTH requirements, respond with either “FALSE:NO QUESTION” or “FALSE:INCOMPLETE QUESTION”.\n'
    multi_prompt += f'Otherwise, respond with “TRUE:” followed immediately by a JSON object containing the user-input-questions. The keys for each user-input-question will be “question”, “question_identifier”, and “answer_identifier”. The identifiers are the opening tag for the corresponding element.\n.'
    multi_prompt += \
"""
Example Response: 'TRUE:[{“question”: “Email Address”,“question_identifier”: “<span class="M7eMe">Email Address</span>”,“answer_identifier”: “<input type="text" class="whsOnd zHQkBf" jsname="YPqjbf" autocomplete="off" tabindex="0" aria-labelledby="i1" aria-describedby="i2 i3" dir="auto" data-initial-dir="auto" data-initial-value="">”},{“question”: “Prod. Date”,“question_identifier”: “<span style="white-space:pre-wrap">Prod. Date</span>”,“answer_identifier”: “<input type="text" class="whsOnd zHQkBf" jsname="YPqjbf" autocomplete="off" tabindex="0" aria-labelledby="i101" aria-describedby="i102 i103" dir="auto" data-initial-dir="auto" data-initial-value="">”}]'
"""
    return multi_prompt


def askGPT4(key, query):
    openai.api_key = key
    message=[{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": query}]
    response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=message,
            temperature=0.5,
            max_tokens=1200,
            frequency_penalty=0.0
        ).choices[0].message.content.strip()
    print("response", response)
    return response


def parseLstOfJsonStrs(s):
    jsons = []
    stack = 0
    curr = ""
    add = False
    for letter in s:
        if letter == "{":
            add = True
            # Ensures only depth 1 curly braces are parsed
            if stack == 0:
                stack += 1
        elif letter == "}":
            stack -= 1
            if stack == 0:
                jsons.append("{"+curr+"}")
                add = False
                curr = ""
        else:
            if add:
                curr += letter
            else:
                pass
    return jsons


def getText(s):
    # a depth stack
    stack = []
    text = ""
    texts = []
    for letter in s:
        if letter in "<{[":
            if not stack:
                texts += [text]
                text = ""
            stack.append(letter)
        elif letter in "}]>":
            if stack:
                stack.pop()
        else:
            if not stack:
                text += letter
    all_text = " ".join(texts)
    all_text = re.sub("[^a-zA-Z| ]", "", all_text).strip()
    return all_text


def question_answer_prompts(id, src, threshold=100):
    """
    Generates prompts for extracting HTML content
    """
    enc = tiktoken.encoding_for_model('gpt-4')
    
    prompts = []

    soup = BeautifulSoup(src, 'html.parser')
    tags = soup.find_all()
    tags = list(map(str, tags))
    tags = sorted(tags, key=lambda x: len(x), reverse=True)
    
    visited = set({})
    for tag in tags:
        text = getText(tag)

        # Skip when element does not contain <input> child node
        if "input" not in tag:
            continue
        # Skip when there is no text present at all
        if not text:
            continue
        if len(enc.encode(text)) > threshold:
            continue
        prompt = getMultiPrompt(text, tag)

        # Very high upper bound
        if len(enc.encode(prompt)) > 1200:
            continue
        # works only when sorted in reverse
        # otherwise, this will skip context
        if text in visited:
            continue
        visited.add(text)
        prompts += [prompt]
    
    return prompts


def question_answer_prompting(identifier, prompts):
    # identifier is openai key for now
    if not identifier:
        return "No identifier"

    responses = []
    visited_questions = {}
    for query_prompt in prompts:
        response = askGPT4(identifier, query_prompt)
        if not response:
            continue
        if response.find("TRUE:") != 0:
            continue
        response_object = load_response(response)
        if not response_object:
            continue

        unique = [item["question"] for item in response_object if item["question"] not in visited_questions]
        duplicates = [item["question"] for item in response_object if item["question"] in visited_questions]
        dd = {}

        # check context
        if not duplicates:
            if unique:
                for item in unique:
                    visited_questions[item] = []
                    responses += response_object
            else:
                # both empty
                pass
        else:
            # add the contexts to the contexts of duplicate questions
            if unique:
                context = " ".join(unique).strip()
                for item in unique:
                    visited_questions[item] = []
                for item in duplicates:
                    dd[item] = "(" + context + ") " + item.strip()

                    # optional data to keep
                    visited_questions[item] += [context]
                
                # add the responses
                for obj in response_object:
                    # add context
                    if newObj["question"] in dd:
                        newObj = obj.copy()
                        newObj["question"] = dd[newObj["question"]]
                        responses.append(newObj)
                    else:
                        responses.append(obj)
            else:
                # Add the data anyways, the have identifiers
                responses += response_object
        
        print(f"{response_object=}\n")        
        responses += response_object
    return responses


