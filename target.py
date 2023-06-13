import re
from bs4 import BeautifulSoup


def getTags(htmlContent):
    soup = BeautifulSoup(htmlContent, "html.parser")
    tags = soup.find_all()
    tags = list(map(str, tags))
    return tags

#
def parseTextSpacing(s):
    words = re.sub("</.+?>", "<[/element]>", s)
    words = re.sub("<.+?>", "<[element]>", words)
    words = re.sub("\n+", "\n", words)
    words = re.sub(" +", " ", words)
    words = " ".join([w.strip() for w in words.split(" ") if w.strip()])
    words = words.strip()
    return words


def addAnswersToDD(dd, tags):
    qas = []
    for key, val in dd.items():
        parentTag = None
        for tag in tags:
            if val[1] in tag and "<input" in tag:
                if not parentTag or len(parentTag) >= len(tag):
                    parentTag = tag
        inputs = BeautifulSoup(parentTag, 'html.parser').find_all('input')
        inputs = list(map(str, inputs))
        dd[key].append(inputs[0])
        # inputs of length 1 constraint:
        # Returns input forms with only one element for answering (No multi-select)
        if len(inputs) == 1:
            qas.append({
            "question": dd[key][0],
            "question_identifier": dd[key][1],
            "answer_identifier": dd[key][2]
            })
    return qas




def question_answer_fast(id, bodyContent):
    tags = getTags(bodyContent)
    questions = {}
    for i, tag in enumerate(tags):
        if len(tag) > 100000: continue
        
        words = parseTextSpacing(tag)
        if 1 <= len(words) < 20:
            if words not in questions:
                questions[words] = [tag, i]
            else:
                if len(questions[words][0]) > len(tag):
                    questions[words] = [tag, i]
    
    # A {i (index of tag from tags): [question: str, tag_identifier (for question): str]}
    dd = {}
    for question, questionHTML in questions.items():
        dd[questionHTML[1]] = [question, questionHTML[0]]

    qas = addAnswersToDD(dd, tags) 
    return qas

