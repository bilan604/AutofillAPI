import re
import json
import openai
from bs4 import BeautifulSoup
from container.src.parsing import getWords


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
                                            temperature=0.20,
                                            max_tokens=4095)

        message = response.choices[0].text.strip()
        return message
    except Exception as e:
        print("Error on OpenAI API Call:", e)
        return None


def contains_duplicate_questions(src):
    # Checks if the same question is asked multiple times
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
            dd[s] += 1
    verdict = False
    for key in dd:
        if dd[key] > 1 and s == re.sub("\^", "", s):
            verdict = True    
    return verdict


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


def getUniqueTags(tags):
    # The entire src
    entireThing = max(tags, key=lambda x: len(x))
    tags = [tag for tag in tags if len(tag) != len(entireThing)]
    # finds tags that are not contained in other tags, reducing recalculation
    uniqueTags = []
    for i, tag in enumerate(tags):
        isUnique = True
        for j in range(len(tags)):
            if i == j:
                continue
            if tag in tags[j]:
                isUnique = False
                break
        if isUnique:
            uniqueTags.append(tag)
    return uniqueTags


def question_answer_prompts(id, bodyContent):
    # A version of question_answer_llm that only returns the prompts
    l,r = bodyContent.find("<body"), bodyContent.find("</body>")
    bodyContent = bodyContent[l:r+len("</body>")]
    
    prompts = []
    stack = [bodyContent]
    while stack:
        newStack = []
        for item in stack:
            if len(item) > 20000:
                tags = list(map(str, BeautifulSoup(item, 'html.parser').find_all()))
                tags = getUniqueTags(tags)
                print("Adding", len(tags), "to stack")
                newStack += tags
            else:
                words = getWords(item).strip()
                text = re.sub("<.+?>", "", words).strip()
                if re.sub(" +", "", text).strip():
                    query_prompt = getMultiPrompt(text, item)
                    prompts.append(query_prompt)
                
        if not newStack:
            return prompts
        stack = newStack

    return prompts


def question_answer_prompting(id, prompts):
    responses = []
    for query_prompt in prompts:
        response = askOpenAI003(id, query_prompt)
        print(f"{response=}\n")
        if response.find("TRUE:") == 0:
            user_input_questions = parseLstOfJsonStrs(response[4:])
            print(f"{user_input_questions=}\n")
            for user_input_question in user_input_questions:
                try:
                    responses.append(json.loads(user_input_question))
                except:
                    print("Could not parse json string:", user_input_question)
    return responses


