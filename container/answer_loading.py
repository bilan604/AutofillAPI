import os
import json
import base64
from container.src.validation import load_credentials



def base64_encode(string):
    # Convert string to bytes
    string_bytes = string.encode('utf-8')
    
    # Encode bytes to base64
    encoded_bytes = base64.b64encode(string_bytes)
    
    # Convert base64 bytes to string
    encoded_string = encoded_bytes.decode('utf-8')
    
    return encoded_string

def base64_decode(encoded_string):
    # Convert base64 string to bytes
    encoded_bytes = encoded_string.encode('utf-8')
    
    # Decode base64 bytes
    decoded_bytes = base64.b64decode(encoded_bytes)
    
    # Convert decoded bytes to string
    decoded_string = decoded_bytes.decode('utf-8')
    
    return decoded_string

#{"id": "testId", "storedResponses": {"name": "John Doe", "first name": "John", "last name": "Doe", "full legal name/full name/name": "John Doe", "email/email address": "john-doe-123@gmail.com", "phone/phone number/mobile number": "1234567890", "address/home address/address line 1": "123 Test s.t.", "state": "California", "country": "United States", "date of birth/D.O.B.": "01/01/1990", "LinkedIn/LinkedIn URL": "https://www.linkedin.com/in/bill-lan-6aaa01147/", "Github/Github URL/Github Link/Portfolio URL/Portfolio Link": "https://github.com/bilan604"}}
def append_question_data(data: str):
    # Takes a stringified json object
    credentials = load_credentials()
    salt = credentials["SALT"].strip()
    line = base64_encode(salt + data)
    with open("src/answers.txt", "a") as f:
        f.write(line + "\n")


def load_question_data(id):
    credentials = load_credentials()
    salt = credentials["SALT"].strip()
    with open("src/answers.txt", "r") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines if l.strip()]
        # ToDo: Add salt
        for item in lines:
            item = base64_decode(item)
            item = item[len(salt):]
            obj = json.loads(item)
            if obj["id"] == id:
                return obj["storedResponses"]
    return None

#dd = {"id": "testId", "storedResponses": {"name": "John Doe", "first name": "John", "last name": "Doe", "full legal name/full name/name": "John Doe", "email/email address": "john-doe-123@gmail.com", "phone/phone number/mobile number": "1234567890", "address/home address/address line 1": "123 Test s.t.", "state": "California", "country": "United States", "date of birth/D.O.B.": "01/01/1990", "LinkedIn/LinkedIn URL": "https://www.linkedin.com/in/bill-lan-6aaa01147/", "Github/Github URL/Github Link/Portfolio URL/Portfolio Link": "https://github.com/bilan604"}}
#append_question_data(json.dumps(dd))