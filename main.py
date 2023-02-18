# Import Google Api Library and required libraries
from apiclient import discovery
import google.auth
import googleapiclient
from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client import client, file, tools

# Scopes asked for oauth. Requesting access to forms and responses
SCOPES = ["https://www.googleapis.com/auth/forms.body.readonly",
          "https://www.googleapis.com/auth/forms.responses.readonly"]

# Google Form I.D. of the Google Form we are using
form_id = "<FORM_ID>"

# API Key - Restricted to Google Forms API v1
developerKey = "<API_KEY>"
DISCOVERY_DOC = f"https://forms.googleapis.com/$discovery/rest?version=v1"

# Store oauth token in a file 'token.json'
store = file.Storage('token.json')
creds = None
# If we do not have credentials, retrieve it from credentials.json
# NOTE: credentials.json was made in the Google Developer Panel
# This will open a link in our browser, requesting permission using the SCOPES initialized earlier.
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

# Standard discovery.build for the Google API
# Retrieves our Google Form information, formatting the questions and responses into lists
def getGoogleFormData():
    forms = build('forms', 'v1', http=creds.authorize(Http()), discoveryServiceUrl = DISCOVERY_DOC, static_discovery=False)
    # Get Google Form information
    form_info = forms.forms().get(formId=form_id).execute()

    # List to hold questions
    questions = []
    # Iterate through the JSON data from the above request (line 35), appending all questions to the list above
    for x in range(len(form_info['items'])):
        questions.append(form_info['items'][x]['title'])
    # Get Google Form responses
    form_responses = forms.forms().responses().list(formId=form_id).execute()
    # Number of responses
    number_of_responses = len(form_responses)
    # Get independant variables
    age_gpt = {'!Question': questions[-1]}

    for x in range(len(form_responses['responses'])):
        if form_responses['responses'][x]['answers']['18cdfc08']['textAnswers']['answers'][0]['value'] not in age_gpt:
            age_gpt[
                form_responses['responses'][x]['answers']['18cdfc08']['textAnswers']['answers'][0]['value']] = {}
            if form_responses['responses'][x]['answers']['4b9d5830']['textAnswers']['answers'][0]['value'] not in age_gpt[form_responses['responses'][x]['answers']['18cdfc08']['textAnswers']['answers'][0]['value']]:
                age_gpt[form_responses['responses'][x]['answers']['18cdfc08']['textAnswers']['answers'][0]['value']][form_responses['responses'][x]['answers']['4b9d5830']['textAnswers']['answers'][0]['value']] = 1
            else:
                age_gpt[form_responses['responses'][x]['answers']['18cdfc08']['textAnswers']['answers'][0]['value']][form_responses['responses'][x]['answers']['4b9d5830']['textAnswers']['answers'][0]['value']] += 1
        else:
            if form_responses['responses'][x]['answers']['4b9d5830']['textAnswers']['answers'][0]['value'] not in age_gpt[form_responses['responses'][x]['answers']['18cdfc08']['textAnswers']['answers'][0]['value']]:
                age_gpt[form_responses['responses'][x]['answers']['18cdfc08']['textAnswers']['answers'][0]['value']][form_responses['responses'][x]['answers']['4b9d5830']['textAnswers']['answers'][0]['value']] = 1
            else:
                age_gpt[form_responses['responses'][x]['answers']['18cdfc08']['textAnswers']['answers'][0]['value']][form_responses['responses'][x]['answers']['4b9d5830']['textAnswers']['answers'][0]['value']] += 1





    pprint(age_gpt)
    # Get dependant variables
            # pprint(form_responses['responses'][x]['answers'][y]['textAnswers']['answers'][0]['value'])
    #pprint(form_responses['responses'])




getGoogleFormData()

