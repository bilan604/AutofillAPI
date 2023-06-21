# AutofillAPI

#### To use this Repository:
1. Git clone this repository
2. Open the folder containing the clone files and make a '.env' file and fill in the fields in '.env.sample'
3. Run app.py

#### To use the chrome extension:
Open Google Chrome, click the three dots in the top right corner (settings), click then manage extensions, make sure developer mode is toggled to on, click load upacked, and select the folder 'Chrome-extension'  

Click on background page to view the console logs.  

To call the api endpoint:
```
import json
import requests


def do_operation(id, operation, data_object):
    ROUTE = "http://127.0.0.1:5000/inputQuestions/"

    # requests must follow this format
    request_json_data = {
        "id": id,
        "operation": operation,
        "requestData": data_object
    }

    response = requests.post(
        url=ROUTE,
        json=json.dumps(request_json_data)
    )

    response_data = json.loads(response.text)
    return response_data
```
