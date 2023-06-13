import re
import os
import time
import base64
import requests
import json
from bs4 import BeautifulSoup
import openai


def getPromptedResponse(content):
    verdicts = []
    for text, words, tag in content:
        if len(text) < 1 or len(tag) < 1: continue
        tag = tag[:min(10000, len(tag))]
        prompt = f'The text following text was found in an html element:\n\"\"\"\n{text}\n\"\"\"\n\n'
        prompt += f'The html contents are:\n\"\"\"\n{tag}\n\"\"\"\n\n'
        prompt += f'Your goal is to identify whether the element contains both the label and input for a single input form question. That is, the element containing the text for the element, the element for user input entry of the response are contained inside the element contents shown above.\n\n'
        prompt += f'If the html element content represents a single Question, Answer Input container element for a single question, respond with \"YES:\" followed immediately by the question. Otherwise, respond with NO: followed immediately by your best estimate of what the html content represents on the webpage.'
        prompt += f'If you are unsure you may respond with "NO:UNSURE".\n'
        prompt += f'Here are some examples of some possible valid responses: "YES:First Name", "YES: Guest email","YES:What days will you attend?", "YES:Forwarding Agent Name", "NO:FORM DESCRIPTION", "NO:NAVIGATION MENU", "NO:UNSURE".\n\n'
        print("----THE PROMPT:\n", prompt)
        response = askOpenAI(prompt, "3")
        print("----THE RESPONSE:\n", response, "\n")
        verdicts.append(response)
    return verdicts


def parseFromVerdicts(verdicts, content):
    response = []
    for verdict, contentElement in zip(verdicts, content):
        verdict = verdict.strip()
        idxYES = verdict.find("YES:")
        idxNO = verdict.find("NO:")
        if not (idxYES == 0 or idxNO == 0):
            continue
        if idxYES != 0: continue
        tag = contentElement[2]
        idxQ = tag.find(">")
        question_indentifier = tag[:min(len(tag), idxQ+1)]
        answer_identifier = ""
        for i in range(len(tag)-len("<input")):
            if tag[i:i+len("<input")] == "<input":
                j = tag[i:].find(">")
                answer_identifier += tag[i:j+1]
        item = {
            "question": " ".join(verdict.split("YES:")[1:]),
            "question_indentifier": question_indentifier,
            "answer_identifier": answer_identifier
        }
        response.append(item)
    return response


def getTags(htmlContent):
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


def getMaxDepth(words):
    lst = [item for item in words.split(" ") if item]
    m = 0
    c = 0
    for item in lst:
        if item == "<[element]>":
            c += 1
        else:
            m = max(m, c)
            c = 0
    return m


def askOpenAI(content_prompt, version=""):
    if len(content_prompt) == 0:
        return "Empty Query Recieved"
    response = ""
    try:
        response = openai.Completion.create(
            model= "text-davinci-003",
            prompt=content_prompt,
            max_tokens=2000,  # Adjust the response length as desired
            temperature=0.25
        ).choices[0].text.strip()

    except:       
        print("Error on OpenAI gpt-3 call")
        return response
    return response


def get_llm_input_questions(id, bodyContent):
    tags = getTags(bodyContent)

    # Count all the possible questions to prevent
    # the same question under different contexts to be asked without context
    counts = {}
    for i, tag in enumerate(tags):
        if len(tag) > 100000: continue
        if tag.find("<div") != 0: continue
        words = getWords(tag.strip()).strip()
        text = re.sub("<.+?>", "", words).strip()
        if text not in counts:
            counts[text] = 0    
        counts[text] += 1      
          
    # Search upstream for context of question if duplicate
    content = []
    for i, tag in enumerate(tags):
        if len(tag) > 100000: continue
        if tag.find("<div") != 0: continue
        # text is plain English
        words = getWords(tag.strip()).strip()
        text = re.sub("<.+?>", "", words).strip()
        if not text: continue
        if counts[text] > 1:
            # either skip
            # try to grab first element of lower nesting depth as context
            minDepth = getMaxDepth(words)
            for j in range(i-1, -1, -1):
                parentWords = getWords(tags[j].strip()).strip()
                parentText = re.sub("<.+?>", "", parentWords).strip()

                if parentText in counts and counts[parentText] == 1 and getMaxDepth(parentWords) > minDepth:
                    context = parentText
                    if not context: continue
                    if context == text: continue
                    content.append([text, context, tag])
                    break
        else:
            content.append([text, words, tag])

    verdicts = getPromptedResponse(content)
    print(f"{verdicts=}\n")
    # Format the responses
    response = parseFromVerdicts(verdicts, content)
    print(f"{response=}\n")
    return response












