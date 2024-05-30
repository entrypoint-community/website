import json
import boto3
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

def get_secret():
    secret_name = "google_drive_service_account"  # Replace with the name of your secret
    region_name = "us-east-1"   # Replace with your AWS region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    # Retrieve the secret value
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    
    # Parse the secret value
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def lambda_handler(event, context):
    # Get service account credentials from AWS Secrets Manager
    credentials_info = get_secret()
    
    # Load the service account credentials JSON data
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info,
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    
    # Set up Google Drive API client
    service = build('drive', 'v3', credentials=credentials)

    # Get the file ID from the event
    file_id = event['file_id']
    print("File ID: ", file_id)

    # Determine the MIME type for export
    mime_type = 'text/plain'  # Export as plain text
    
    # Export the file content
    request = service.files().export_media(fileId=file_id, mimeType=mime_type)
    file_content = io.BytesIO()
    downloader = MediaIoBaseDownload(file_content, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    file_content.seek(0)
    
    # Process the file content
    contacts_str = file_content.read().decode('utf-8').lstrip('\ufeff')
    print("Contacts string: ", contacts_str)
    
    # Create the JSON payload
    payload = {
        'contacts': contacts_str
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(payload)
    }


