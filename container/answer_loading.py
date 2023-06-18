import os
import json
import base64

"""
This file contains handler functions for information. Not required or implemented yet.
Currently there is a data folder containing the question-answer information that
parses them as CSVs.
"""
# ChatGPT
def base64_encode(string):
    # Convert string to bytes
    string_bytes = string.encode('utf-8')
    
    # Encode bytes to base64
    encoded_bytes = base64.b64encode(string_bytes)
    
    # Convert base64 bytes to string
    encoded_string = encoded_bytes.decode('utf-8')
    
    return encoded_string

# ChatGPT
def base64_decode(encoded_string):
    # Convert base64 string to bytes
    encoded_bytes = encoded_string.encode('utf-8')
    
    # Decode base64 bytes
    decoded_bytes = base64.b64decode(encoded_bytes)
    
    # Convert decoded bytes to string
    decoded_string = decoded_bytes.decode('utf-8')
    
    return decoded_string


def load_question_data(id):
    salt = os.getenv("SALT")
    # ToDo: implement this function
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

