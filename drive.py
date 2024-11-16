import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
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
    """
    Search for a file by name in a Google Drive folder (including shared files).

    :param service: Authenticated Google Drive API service.
    :param folder_id: ID of the folder to search in.
    :param file_name: Name of the file to search for.
    :return: ID of the file if found, None otherwise.
    """
    try:
        query = f"'{folder_id}' in parents and name = '{file_name}' and trashed = false"
        # Include files shared with the authenticated user
        response = service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)',
            supportsAllDrives=True,  # Include shared drives
            includeItemsFromAllDrives=True
        ).execute()
        files = response.get('files', [])
        
        if not files:
            print(f"File '{file_name}' not found in folder '{folder_id}'.")
            return None

        print(f"File '{file_name}' found with ID: {files[0]['id']}")
        return files[0]['id']
    except HttpError as error:
        print(f"An error occurred while searching for the file: {error}")
        return None


import gdown

def download_file_gdown(file_id, destination_path):
    """
    Download a file from Google Drive using gdown.

    :param file_id: ID of the file to download.
    :param destination_path: Path where the file should be saved.
    """
    try:
        # Construct the gdown download URL
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, str(destination_path), quiet=False)
        print(f"File downloaded successfully to {destination_path}.")
    except Exception as error:
        print(f"An error occurred while downloading the file: {error}")
        raise


def download_file(service, file_id, destination_path):
    """
    Download a file from Google Drive and save it to the specified destination.
    
    :param service: Authenticated Google Drive API service.
    :param file_id: ID of the file to download.
    :param destination_path: Path where the file should be saved.
    """
    try:
        request = service.files().get_media(fileId=file_id)
        with open(destination_path, "wb") as file:
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download progress: {int(status.progress() * 100)}%")
    except HttpError as error:
        print(f"An error occurred while downloading the file: {error}")
