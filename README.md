# AutofillAPI

#### To use this Repository:
1. Git clone this repository
2. Open the folder containing the clone files and make a '.env' file and fill in the fields in '.env.sample'
3. install the dependencies in the directory using pip
3. Run using python main.py

#### To use the chrome extension:
Open Google Chrome, click the three dots in the top right corner (settings), click then manage extensions, make sure developer mode is toggled to on, click load upacked, and select the folder 'Chrome-extension'  

Click on background page to view the console logs.  

Here is an example of the loaded LLM output, which gets deduplicated and contextualized. 
```
[
    {'question': 'Forwarding Agent', 
    'question_identifier': '<label class=input-group-text for=CMForwarder\\>Forwarding Agent</label>', 
    'answer_identifier': '<input autocomplete=off class=form-control data-docit-input=true id=CMForwarder/>'}, 
    {'question': 'Address', 
    'question_identifier': '<label class=input-group-text\\>Address*</label>', 
    'answer_identifier': ''}, 
    {'question': 'Name', 
    'question_identifier': '<label class=input-group-text\\>Name</label>', 
    'answer_identifier': '<input class=form-control data-docit-input=true id=CMForwarderName/>'}, 
    {'question': 'Email', 
    'question_identifier': '<label class=input-group-text\\>Email</label>', 
    'answer_identifier': '<input class=form-control data-docit-input=true id=CMForwarderEmail/>'}, 
    {'question': 'Phone', 
    'question_identifier': '<label class=input-group-text\\>Phone</label>', 
    'answer_identifier': '<input class=form-control data-docit-input=true id=CMForwarderPhone/>'}, 
    {'question': 'Fax', 
    'question_identifier': '<label class=input-group-text\\>Fax</label>', 
    'answer_identifier': '<input class=form-control data-docit-input=true id=CMForwarderFax/>'}, 
    {'question': 'Shipper', 
    'question_identifier': '<label class=input-group-text for=CMShipper\\>Shipper*</label>', 
    'answer_identifier': '<input autocomplete=off class=form-control data-docit-input=true id=CMShipper/>'}, 
    {'question': 'Address', 
    'question_identifier': '<label class=input-group-text\\>Address*</label>', 
    'answer_identifier': ''}, 
    {'question': 'Name', 
    'question_identifier': '<label class=input-group-text\\>Name</label>', 
    'answer_identifier': '<input class=form-control data-docit-input=true id=CMShipperName/>'},
    {'question': 'Email', 
    'question_identifier': '<label class=input-group-text\\>Email</label>', 
    'answer_identifier': '<input class=form-control data-docit-input=true id=CMShipperEmail/>'}, 
    {'question': 'Phone', 
    'question_identifier': '<label class=input-group-text\\>Phone</label>', 
    'answer_identifier': '<input class=form-control data-docit-input=true id=CMShipperPhone/>'}, 
    {'question': 'Fax', 
    'question_identifier': '<label class=input-group-text\\>Fax</label>', 
    'answer_identifier': '<input class=form-control data-docit-input=true id=CMShipperFax/>'}
]
```

