import json
import boto3
import requests
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    # we need to Define the real CloudWatch metric to retrieve
    metric_name = 'InterviewCount'
    namespace = 'Interviews'
    company_name = event.get('company_name')
    interview_date = event.get('interview_date')
    
    if not company_name or not interview_date:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid input: company_name and interview_date are required.')
        }

    try:
        interview_date = datetime.strptime(interview_date, '%Y-%m-%d')
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid date format. Use YYYY-MM-DD.')
        }

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)  

    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=[
            {
                'Name': 'CompanyName',
                'Value': company_name
            },
            {
                'Name': 'InterviewDate',
                'Value': interview_date.strftime('%Y-%m-%d')
            }
        ],
        StartTime=start_time,
        EndTime=end_time,
        Period=3600, 
        Statistics=['Sum']
    )
    
    data_points = response['Datapoints']
    if not data_points:
        return {
            'statusCode': 200,
            'body': json.dumps('No data points found for the specified time range.')
        }

    interview_count = data_points[0]['Sum']
    
    # we need to Define the URL of the website endpoint
    website_url = 'https://yourwebsite.com/api/metrics'  
    
    payload = {
        'company_name': company_name,
        'interview_date': interview_date.strftime('%Y-%m-%d'),
        'interview_count': interview_count
    }
    
    response = requests.post(website_url, json=payload)
    
    if response.status_code == 200:
        return {
            'statusCode': 200,
            'body': json.dumps('Metric data successfully sent to the website.')
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': json.dumps('Failed to send metric data to the website.')
        }
