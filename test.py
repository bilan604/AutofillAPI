
def getPromptedResponse(content):
    verdicts = []
    for text, words, tag in content:
        if len(text) < 1 or len(tag) < 1: continue
        tag = tag[:min(10000, len(tag))]
        prompt = getMultiPrompt(text, tag)
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


