import json
import os
import boto3
from botocore.exceptions import ClientError
import psycopg2
from psycopg2 import OperationalError
from credentials import db_creds

# get the credentials for Secret Manager
def getCredentials() -> db_creds:

    client = boto3.client(
      service_name='secretsmanager',
      region_name=os.environ['AWS_REGION']
    )
    
    try:
        secret_value = client.get_secret_value(
            SecretId='secretName' # replace with the real secret name 
        )
        secret = json.loads(secret_value['SecretString'])
    except ClientError as e:
        print(f"The error '{e}' occurred")
        raise e
    
    return db_creds(
        username = secret['username'],
        password = secret['password'],
        host = secret['host'],
        database = secret['database']
    )


def lambda_handler(event, context):
  
    try:
        credential = getCredentials()
    except json.JSONDecodeError as e:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({"error": "Invalid JSON syntax", "message": str(e)})
            }
    
    # try to connect to the DB
    try:
        connection = psycopg2.connect(
            user=credential.username,
            password=credential.password,
            host=credential.host,
            database=credential.database,
            connect_timeout=10
        )
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"error": "Database connection failed", "message": str(e)})
        }

    try:  
        cursor = connection.cursor()
        
        check_table = "SELECT 1 FROM pg_tables WHERE tablename = 'users'"
        cursor.execute(check_table)
        table_exists = cursor.fetchone()

        if not table_exists:
            print("There is no table called 'users'")
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({"message": "There is no table called 'users'"})
            }
        
        query = "SELECT * FROM users"
        cursor.execute(query)
        
        user_data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(user_data)
        }

    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"error": str(e)})
        }
    except Exception as error:
        print(f"Error occurred: {error}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({"error": str(error)})
        }