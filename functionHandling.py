import json
from target import question_answer_fast
from answering import answer_input_questions
from advance import question_answer_prompts, question_answer_prompting


def doQuestionAnswerLLM(id, data):
    htmlContent = data["requestData"]
    prompts = question_answer_prompts(id, htmlContent)
    responses = question_answer_prompting(id, prompts)
    return json.dumps(responses)

def doQuestionAnswerPrompts(id, data):
    htmlContent = data["requestData"]
    prompts = question_answer_prompts(id, htmlContent)
    return json.dumps(prompts)

def doQuestionAnswerPrompting(id, data):
    prompts = data["requestData"]
    responses = question_answer_prompting(id, prompts)
    return json.dumps(responses)

def doQuestionAnswerFast(id, data):
    htmlContent = data["requestData"]
    qas = question_answer_fast(id, htmlContent)
    return json.dumps(qas)

def doQuestionAnswerFast2(id, data):
    htmlContent = data["requestData"]
    qas = question_answer_fast(id, htmlContent, False)
    return json.dumps(qas)

def doAnswerInputQuestions(id, data):
    qas = data["requestData"]
    answers = answer_input_questions(id, qas)
    return json.dumps(answers)

