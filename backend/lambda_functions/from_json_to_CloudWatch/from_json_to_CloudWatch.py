import json
import boto3
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize CloudWatch client
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    try:
        # Log the received event
        logger.info(f"Received event: {json.dumps(event)}")
        
        # Extract information from the event
        company_name = event['company_name']
        interview_date = event['interview_date']
        
        # Define the metric data
        metric_name = "InterviewCount"
        metric_value = 1  # You can set this to any value you prefer
        namespace = "Interviews"  
        dimensions = [
            {
                'Name': 'CompanyName',
                'Value': company_name
            },
            {
                'Name': 'InterviewDate',
                'Value': interview_date
            }
        ]
        
        # Put the metric data to CloudWatch
        response = cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': dimensions,
                    'Value': metric_value,
                    'Unit': 'Count'  
                },
            ]
        )
        
        # Log the response from CloudWatch
        logger.info(f"CloudWatch put_metric_data response: {response}")
        
        return {
            'statusCode': 200,
            'headers': {
            'Access-Control-Allow-Origin': '*',  
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Methods': 'GET,OPTIONS,POST,PUT'
            },
            'body': json.dumps('Metric data put successfully')
        }
        
    except Exception as e:
        logger.error(f"Error putting metric data: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error putting metric data')
        }