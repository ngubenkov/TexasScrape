import pickle
import os.path
import os
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = 'https://www.googleapis.com/auth/drive'
UPLOAD_DIRECTORY = 'screenshots/'

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/korouf/Downloads/client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # store = file.Storage('storage.json')
    # creds = store.get()
    # if not creds or creds.invalid:
    #     flow = client.flow_from_clientsecrets('/Users/korouf/Downloads/client_secret.json', SCOPES)
    #     creds = tools.run_flow(flow, store)
    # service = discovery.build('drive', 'v3', http=creds.authorize(Http()))

    service = build('drive', 'v3', credentials=creds)
    FILES= []
    with os.scandir(UPLOAD_DIRECTORY) as allfiles:
        for each in allfiles:
            if each.is_file() and not each.name.startswith('.'):
                print(each.name)
                FILES.append((each.name, None))
    # Call the Drive v3 API

    for filename, mimeType in FILES:
        metadata = {'name': filename}
        if mimeType:
            metadata['mimeType'] = mimeType
        res = service.files().create(body=metadata, media_body=UPLOAD_DIRECTORY+ filename).execute()
        if res:
            print('Uploaded "%s"' % filename)


if __name__ == '__main__':
    main()