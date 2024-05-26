import json
import boto3
from botocore.exceptions import ClientError
import psycopg2
from psycopg2 import OperationalError


def getCredentials():
    credential = {}
    
    secret_name = "mysecretname"
    region_name = "us-east-1"
    
    client = boto3.client(
      service_name='secretsmanager',
      region_name=region_name
    )
    
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested failed due to permmisions issue")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
        elif e.response['Error']['Code'] == 'DecryptionFailure':
            print("The requested secret can't be decrypted using the provided KMS key:", e)
        elif e.response['Error']['Code'] == 'InternalServiceError':
            print("An error occurred on service side:", e)

    else:
      secret = json.loads(get_secret_value_response['SecretString'])
      
      credential['username'] = secret['username']
      credential['password'] = secret['password']
      credential['host'] = "host"
      credential['db'] = "databasename"
    
    return credential

def lambda_handler(event, context):
  credential = getCredentials()
  
  connection = psycopg2.connect(
      user=credential['username'], 
      password=credential['password'], 
      host=credential['host'], 
      database=credential['db']
  )
  try:  
        cursor = connection.cursor()
        
        check_table = "SELECT 1 FROM pg_tables WHERE tablename = 'users'"
        cursor.execute(check_table)
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("There is no table called 'users'")
            return {'statusCode': 400, 'message': "There is no table called 'users'"}
        
        query = "SELECT * FROM users"
        cursor.execute(query)
        
        results = cursor.fetchall()
        
        cursor.close()
        connection.close()
        
        return {'statusCode': 200, 'body': results}

  except OperationalError as e:
      print(f"The error '{e}' occurred")
      return {'statusCode': 500, 'error': str(e)}
  except Exception as error:
      print(f"Error occurred: {error}")
      return {'statusCode': 500, 'error': str(error)}