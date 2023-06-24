import re
import json
from bs4 import BeautifulSoup


def contains_url(string):
    pattern = r"[http[s]?://]?[www\.]?[a-zA-Z|0-9]{3,30}[\.][a-z]{3,20}[(/a-z)]?"
    match = re.search(pattern, string)
    return bool(match)


def getTags(htmlContent):
    if htmlContent.find("<body") != 0:
        soup = BeautifulSoup(htmlContent, "html.parser")
        htmlContent = str(soup.find_all("body")[0])
        
    soup = BeautifulSoup(htmlContent, "html.parser")
    tags = soup.find_all()
    tags = list(map(str, tags))
    return tags


def getWords(s):
    words = re.sub("<\\//.+?>", "<[/element]>", s)
    words = re.sub("<.+?>", "<[element]>", words)
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = " ".join([w.strip() for w in words.split(" ") if w.strip()])
    words = words.strip()
    return words


def parseAnswerTextSpacing(s):
    # Lowercase version
    words = re.sub("-", " ", s.lower().strip())
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = words.strip()
    return words


def remove_escape_sequences(qa):
    newQa = ""
    for i in range(len(qa)):
        letter = qa[i]
        if letter == "\\":
            if i == 0:
                pass
            elif i == len(qa) - 1:
                pass
            else:
                if not (qa[i-1] == "<" or qa[i+1] == ">"):
                    pass
                else:
                    newQa += letter
        else:
            newQa += letter
    return newQa.strip()


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


def handle_parse_json(qa, expected_keys=3):
    # parses a json object
    if len(qa) < 2:
        return None
    dd = {}
    qa = qa[1:-1]
    qa = qa.split(",")
    qa = [qa.split(":") for qa in qa]
    qa = [q_a for q_a in qa if len(q_a) == 2]
    if len(qa) != expected_keys:
        return None
    qa = [[q_a[0].strip(), q_a[1].strip()] for q_a in qa]
    for q_a in qa:
        if not q_a[0] or not q_a[1]:
            return None
        k = re.sub("\"", "", q_a[0])
        k = remove_escape_sequences(k)
        v = re.sub("\"", "", q_a[1])
        v = remove_escape_sequences(v)
        dd[k] = v
    return dd


def load_response(response):
    response = "".join(response.split("TRUE:")[1:])
    response_object = parseLstOfJsonStrs(response)
    loaded_responses = []
    for question_answer in response_object:
        question_answer = handle_parse_json(question_answer)
        if not question_answer:
            continue
        loaded_responses.append(question_answer)
    return loaded_responses