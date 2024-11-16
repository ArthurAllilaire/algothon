import io
import os
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
import io
from google.oauth2.credentials import Credentials

from googleapiclient.http import MediaIoBaseDownload
# Google Drive API authentication
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FOLDER_ID = '1ElVOO_4Plr24xEOmdqsINmIRM_y4M3_n'

def authenticate_google_drive():
    """Authenticate and build the Google Drive API client."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def find_file_in_folder(service, folder_id, file_name):
    """Search for a file by name inside a Google Drive folder."""
    query = f"'{folder_id}' in parents and name = '{file_name}'"
    try:
        results = service.files().list(q=query).execute()
        items = results.get('files', [])
        
        if not items:
            print(f'No file found with name {file_name} in folder {folder_id}.')
            return None
        else:
            # There could be multiple files with the same name, but we’ll pick the first one
            item = items[0]  # Assuming the file name is unique
            file_id = item['id']
            file_name = item['name']
            print(f'Found file: {file_name} with ID: {file_id}')
            return file_id
    except Exception as e:
        print(f"An error occurred while searching for the file: {e}")
        return None


def download_file(service, file_id, destination_path):
    """Download a file from Google Drive using its file ID."""
    try:
        # Request the file from Google Drive
        request = service.files().get_media(fileId=file_id)
        
        # Create a file handle to save the file
        fh = io.FileIO(destination_path, 'wb')
        
        # Download the file to the specified destination
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")
        
        print(f"File downloaded to {destination_path}.")
    except Exception as e:
        print(f"An error occurred while downloading the file: {e}")
