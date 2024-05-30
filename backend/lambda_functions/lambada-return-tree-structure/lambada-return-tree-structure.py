import json
import os
import boto3
import base64
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials from environment variables or AWS Secrets Manager
def get_google_drive_service():
    # Assuming the credentials are stored in AWS Secrets Manager
    secret_name = os.environ['GOOGLE_CREDENTIALS_SECRET']
    region_name = os.environ['AWS_REGION']

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        secret = get_secret_value_response['SecretString']
        credentials_info = json.loads(secret)
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        raise e

    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    service = build('drive', 'v3', credentials=credentials)
    return service

def list_drive_files(service, folder_id='root'):
    query = f"'{folder_id}' in parents and trashed=false"
    results = service.files().list(
        q=query,
        pageSize=1000,
        fields="nextPageToken, files(id, name, mimeType, webViewLink)"
    ).execute()

    items = results.get('files', [])
    tree = {}
    for item in items:
        if item['mimeType'] == 'application/vnd.google-apps.folder':
            tree[item['name']] = {
                'id': item['id'],
                'link': item['webViewLink'],
                'children': list_drive_files(service, item['id'])
            }
        else:
            tree[item['name']] = {
                'id': item['id'],
                'link': item['webViewLink']
            }
    return tree

def lambda_handler(event, context):
    try:
        service = get_google_drive_service()
        drive_tree = list_drive_files(service)
        return {
            'statusCode': 200,
            'body': json.dumps(drive_tree)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
