import json
import psycopg2
import os
import boto3

# Environment Variables
REGION = os.environ['REGION']
DB_HOST = os.environ['DB_HOST']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']
WHATSAPP_LINK = "https://chat.whatsapp.com/Bx3hIysSqmG5p3ZYtnNXw7"

# Initialize the SES client
ses = boto3.client('ses', region_name=REGION)

# Database connection function
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print("Error connecting to the database: ", e)
        raise

# Execute a given query with the given parameters
def execute_query(query, params):
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error executing query: ", e)
        raise

# Send an email to the user
def send_email(to_address, name):
    try:
        response = ses.send_email(
            Source="email@domain.com", # Replace with your email
            Destination={
                'ToAddresses': [to_address]
            },
            Message={
                'Subject': {
                    'Data': 'Welcome to the Entrypoint - Community',
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': f'Hello {name},\n\nThank you for joining the community. You can join our WhatsApp group using the following link: {WHATSAPP_LINK}\n\nBest,\nCommunity Team',
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        print("Email sent successfully to ", to_address)
    except Exception as e:
        print("Error sending email: ", e)
        raise

# Lambda handler
def lambda_handler(event, context):
    try:
        user_data = json.loads(event['body'])
        name = user_data['name']
        email = user_data['email']
        phone = user_data['phone']
    except Exception as e:
        print(f"Error parsing event data: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps('Bad Request')
        }
    
    # Insert via query into the database
    try:
        query = "INSERT INTO community_members (name, email, phone) VALUES (%s, %s, %s)"
        params = (name, email, phone)
        execute_query(query, params)
    except Exception as e:
        print(f"Error inserting data into the database: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
    
    # Send email to the user
    try:
        send_email(email, name)
    except Exception as e:
        print(f"Error sending email: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }

