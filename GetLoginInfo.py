from apiclient import discovery
from httplib2 import Http
from oauth2client import file
from oauth2client import client
from oauth2client import tools

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = 'REDACTED'
DISCOVERY_DOC = 'REDACTED'
DOCUMENT_ID = 'REDACTED'

def get_credentials():
    store = file.Storage('token.json')
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        credentials = tools.run_flow(flow, store)
    return credentials

def read_paragraph_element(element):
    text_run = element.get('textRun')
    if not text_run:
        return ''
    return text_run.get('content')


def read_strucutural_elements(elements):
    text = ''
    for value in elements:
        if 'paragraph' in value:
            elements = value.get('paragraph').get('elements')
            for elem in elements:
                text += read_paragraph_element(elem)
        elif 'table' in value:
            table = value.get('table')
            for row in table.get('tableRows'):
                cells = row.get('tableCells')
                for cell in cells:
                    text += read_strucutural_elements(cell.get('content'))
        elif 'tableOfContents' in value:
            toc = value.get('tableOfContents')
            text += read_strucutural_elements(toc.get('content'))
    return text

def getLoginInfo():
    credentials = get_credentials()
    http = credentials.authorize(Http())
    docs_service = discovery.build('docs', 'v1', http=http, discoveryServiceUrl=DISCOVERY_DOC)
    doc = docs_service.documents().get(documentId=DOCUMENT_ID).execute()
    doc_content = doc.get('body').get('content')
    return(read_strucutural_elements(doc_content))

def send_acc_details(details):
    creds = ""
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=get_credentials())

    requests = [
             {
                'insertText': {
                    'location': {
                        'index': 18
                    },
                    'text': " <+> " + details
                }
            }
        ]

    result = service.documents().batchUpdate(documentId=DOCUMENT_ID, body={'requests': requests}).execute()