# Steps needs to take to run the lambda function
# 1. Setting up the RDS Postgres Database
# 2. Setting up IAM Role so that the lambda function can access the RDS Postgres Database

import json
import psycopg2
import os
import boto3
import os 

# Environment Variables
REGION=os.environ['REGION']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']
WHATSAPP_LINK = os.environ['WHATSAPP_LINK']

# Initalize the SES to send the email
# ses = boto3.client('ses', region_name=REGION)

def lambda_handler(event, context):
    # extract the data from the event
    user_data = json.loads(event['body'])
    name = user_data['name']
    email = user_data['email']
    phone = user_data['phone']

    # Connect to the database
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()

    # Inserting userdata into db (assumes table is already created and called community_members)
        cursor.execute("INSERT INTO community_members (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
    
    # TODO: implement the email sending logic

