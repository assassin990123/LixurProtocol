from __future__ import print_function
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import os.path
import pickle
import json
import io
import os

class Cloud:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/drive']
        self.service = self.Create_Service('credentials.json', 'Drive', 'v3', self.scopes)

    def Create_Service(self, client_secret_file, api_name, api_version, *scopes):
        client_secret_file = client_secret_file
        api_service_name = api_name
        api_version = api_version
        scopes = [scope for scope in scopes[0]]

        cred = None

        pickle_file = f'token_{api_service_name}_{api_version}.pickle'

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(api_service_name, api_version, credentials=cred)
            print('Google Cloud Service initiated successfully!')
            return service
        except Exception as e:
            print('Unable to connect.')
            print(e)
            return None

    def view_files_in_drive(self):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('drive', 'v3', credentials=creds)

            # Call the Drive v3 API
            results = service.files().list(
                pageSize=10, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
            print('Files:')
            for item in items:
                print(u'{0} ({1})'.format(item['name'], item['id']))
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')

    def scan_for_existing_files(self):
        page_token = None
        self.existing_file = False

        while True:
            response = self.service.files().list(q="mimeType='text/plain'", spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
            for file in response.get('files', []):
                self.file_id = file.get('id')
                self.file_name = file.get('name')
                self.existing_file = True
            page_token = response.get('nextPageToken', None)

            if page_token is None:
                break

    def upload_peer_list(self):
        service = self.service
        folder_id = "1KQ101rSKnN-ifK3daysh1qZ1G3wZGNwE"
        file_names = ["source/peers.txt"]
        mime_types = ["text/plain"]

        for filename, mimetype in zip(file_names, mime_types):
            file_metadata = {
                'name': filename,
                'parents': [folder_id]
            }

            self.scan_for_existing_files()

            if self.existing_file:
                media = MediaFileUpload(filename, mimetype)
                service.files().update(fileId=self.file_id, body=None, media_body=media, fields='id, name').execute()
            else:
                media = MediaFileUpload(filename, mimetype)
                service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    def download_peer_list(self):
        service = self.service
        self.scan_for_existing_files()

        request = service.files().get_media(fileId=self.file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while done is False:
            status, done = downloader.next_chunk()
        fh.seek(0)
        data_on_file = fh.read().decode('utf-8')

        with open('source/peers.txt', 'w+') as f:
            f.write(data_on_file)

    def add_self_to_peer_list(self):
        with open("source/info.json", 'r') as f:
            data = eval(f.read())
            server_ip = data[0]
            server_port = data[1]
            session_id = data[2]
            total = server_ip, server_port, session_id
            load = list(total)
            f.close()

        self.download_peer_list()

        with open('source/peers.txt', 'r+') as f:
            data = eval(f.read())
            data.append(load)
            f.seek(0)
            json.dump(data, f)

        self.upload_peer_list()
        self.download_peer_list()