# Project Translator
Translator is a web application written in python to translate restaurant working hours into human readable format. Request to this app can be made using curl or any http client like postman.

For license, see the LICENSE file. 

Author: Sandesh P V

### Requirements:
1. Python 3.8
2. python3-venv
3. setuptools

### Verified Testing environments:
1. macOs Big Sur (11.5.2)
2. Ubuntu 16.04 x64

### Package Structure:
```
├── LICENSE
├── README.md
├── setup.py
├── src
│   └── datatranslator
│       ├── apierror.py
│       ├── app.py
│       ├── config.py
│       ├── __init__.py
│       ├── pyproject.toml
│       └── translator.py
└── tests
    ├── fixtures.py
    ├── test_app.py
    └── test_translator.py
```

Main files:
README.md: This file
src/datatranslator/app.py: flask route for API
src/datatranslator/translator.py: Date translator
src/datatranslator/apierror.py: App specific exception handler
src/datatranslator/config.py: App specific configs

### How to run:
NOTE: Ensure you have the correct version before proceeding:
sandesh@sandesh:~/projects/traslator$ python --version
Python 3.8.7

Open CLI and perform the following:
1. unzip translator.zip (extract package)
2. cd translator (Go to the package directory)
3. python3 -m venv venv/ (Create python environment) Note: Ensure to choose specific python 3 binary if there are multiple (eg: python3.8)
4. source venv/bin/activate (Activate the virtual environment)
5. python setup.py install (Install dependencies) Note: It may take some time based on the environment
6. python -m pip install . (Optional: Install the application to current directory)
    Note: If not installing, Can run the app from source directory: python src/datatranslator/app.py
7. python ./venv/lib/python-<version>/site-packages/datatranslator/app.py (start the application)
   Example: python ./venv/lib/python-3.8/site-packages/datatranslator/app.py

Note: Server will be running on port 5001. If it is unavailble, then update the appropriate port in config.py and reinstall the app (Step - 6)

### Changing basic configurations:
Basic configurations such as port, enabling deubg can be set from `config.py`

### Testing:
Server will be listeneing on `/restaurant/dates` on configured port (default 5001). This endpoint supports only POST and requests can be send using normal http clients such as postman or curl:

curl --form "file=@dates.json" http://localhost:5001/restaurant/dates

whereas it takes a form parameter file which is the name of the file that contains the request json in the following format as specified in the problem statement:

```
{
    "monday": [],
    "tuesday": [
        {
            "type": "open",
            "value": 36000
        },
        {
            "type" : "close",
            "value": 64800
        }
    ],
    ...
}
```

Output will be printed in the console as mentioned in the problem statement:

```
Monday: Closed
Tuesday: 10 AM - 6 PM
Wednesday: Closed
Thursday: 10:30 AM - 6 PM
Friday: 10 AM - 1 AM
Saturday: 10 AM - 1 AM
Sunday: 12 PM - 9 PM
```

Please note, the same will be send back to the client in the form of a list:
[
  "Monday: Closed", 
  "Tuesday: 10 AM - 6 PM", 
  "Wednesday: Closed", 
  "Thursday: 10:30 AM - 6 PM", 
  "Friday: 10 AM - 1 AM", 
  "Saturday: 10 AM - 1 AM", 
  "Sunday: 12 PM - 9 PM"
]

### Unit testing:
tests are located inside tests folder and can be run using pytest:
python -m pytest tests/*

tests/test_app.py ...
tests/test_translator.py ....

# PART - 2: Thoughts on Input JSON:
1. Input data in its current form is not extendible. We can't process it say for a month.

2. I am of the openion of considering a day as a complete logical object without overlapping, that makes it easier to translate 
without much checks and most of the programming languages such as Java supports json to POJO mapping and converting them into a different format (such as HumanReadable should be cleaner). Also, Validation support such as [jsr 380](https://en.wikipedia.org/wiki/Bean_Validation) are built in as part of frameworks like spring and hibernate makes it easier to control tolerance levels and keeps the core logic much cleaner.

One approach would be this: 

```
{
    "days": [
        {
            "date": "7",
            "month": "09",
            "day": "Wednesday",
            "hours": [
                {
                    "type": "open",
                    "value": 36000
                },
                {
                    "type": "close",
                    "value": 64800
                }
            ]
        }
    ]
}
```
Downside here is since we know there are only 7 days, we can have a fixed number of objects. But if there is a need to generate say 30 days 
schedule, this would be useful than the original one as objects like Monday cannot be duplicated.
