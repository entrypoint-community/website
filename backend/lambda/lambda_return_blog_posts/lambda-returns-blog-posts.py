from lambdaRetrieveDataLibrary.lambda_return_data import get_postgres_credentials,check_table
import json
import os
import psycopg2
from psycopg2 import OperationalError, sql

def lambda_handler(event, context):
    try:
        credential = get_postgres_credentials(secret_Name=os.environ["secret_name"]) # replace the secret with the actual secret for the DB creds
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
        
        query = sql.SQL("SELECT * FROM blog_posts")
        cursor.execute(query)
        
        table_data = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps(table_data)
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