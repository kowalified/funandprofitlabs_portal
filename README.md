# Portal 2.0 for the Fun and Profit Labs @ Ciscolive
Verison 2.0 of the portal used in the 'fun and (fake) profit' lab series at the [CiscoLive](https://www.ciscolive.com/global/) conference. Hosted at sessions: LTRRST-1179 and LTRRST-2016.

## Install instructions
Notes:
* By default, webserver is set to run on port 8000. 

### Notes
Ran the following in root folder to setup virtualenv (on OSX) to reduce errors within vscode:
```
virtualenv venv
source venv/bin/activate
python venv/bin/pip install -r requirements.txt
python venv/bin/pip install pep8 pylint
deactivate
```

## To-do
* Double check emails
* Display student port numbers based on student number
* Ensure students cannot have the same student number
* Validate student number when existing user logs in
* Clean up unused code
* Complete installation instructions
