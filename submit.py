import pandas as pd
import cryptpandas as crp
from time import time
import re
from pathlib import Path
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import gdown
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env files - will share with you dylan

# Load the encrypted file to df
def load_encrypted() -> pd.DataFrame:


    # Get the path and password from slack
    file_name, password = get_file_name_and_password()
    path = Path('decrypted_data') / file_name
    
    # get the file on google drive
    
    url = "https://drive.google.com/drive/folders/1ElVOO_4Plr24xEOmdqsINmIRM_y4M3_n"

    # Load the CSV file
    return crp.read_encrypted(path=path, password=password)


    
# get password from slack


def get_file_name_and_password():
    # Replace with your OAuth token
    client = WebClient(token=os.getenv("SLACK_API_TOKEN"))

    # Replace with the ID of the channel you want to fetch messages from
    channel_id = "C080P6M4DKL"

    try:
        # Fetch messages from the channel
        response = client.conversations_history(channel=channel_id, limit=100, oldest=round(time() - 60*19, 6))
        messages = response['messages']
        
        for msg in messages:
            if msg.get('user') == 'U080GCRATP1':
                pattern = r"'([^']+\.crypt)'.*'([^']+)'"
                match = re.search(pattern, msg.get('text'))
                if match:
                    file_name = match.group(1)
                    password = match.group(2)
                    print(f"File: {file_name} - Password: {password} - Time: {msg.get('ts')}")
                    return file_name, password
        else:
            print("No message found")
            return None, None

    except SlackApiError as e:
        print(f"Error fetching messages: {e.response['error']}")
        return None, None
