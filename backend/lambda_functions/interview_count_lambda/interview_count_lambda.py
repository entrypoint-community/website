import json
import boto3
import requests
from datetime import datetime, timedelta

cloudwatch = boto3.client('cloudwatch')

def validate_input(event):
    company_name = event.get('company_name')
    interview_date = event.get('interview_date')
    
    if company_name and interview_date:
        try:
            interview_date = datetime.strptime(interview_date, '%Y-%m-%d')
        except ValueError:
            return False, 'Invalid date format. Use YYYY-MM-DD.'
    
    return True, (company_name, interview_date)

def get_metric_statistics(company_name=None, interview_date=None):
    namespace = 'Interviews'
    metric_name = 'InterviewCount'
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=1)
    
    dimensions = []
    if company_name:
        dimensions.append({'Name': 'CompanyName', 'Value': company_name})
    if interview_date:
        dimensions.append({'Name': 'InterviewDate', 'Value': interview_date.strftime('%Y-%m-%d')})
    
    response = cloudwatch.get_metric_statistics(
        Namespace=namespace,
        MetricName=metric_name,
        Dimensions=dimensions,
        StartTime=start_time,
        EndTime=end_time,
        Period=3600,
        Statistics=['Sum']
    )
    
    return response['Datapoints']

def send_metric_to_website(company_name, interview_date, interview_count):
    website_url = 'https://yourwebsite.com/api/metrics'
    payload = {
        'company_name': company_name,
        'interview_date': interview_date.strftime('%Y-%m-%d'),
        'interview_count': interview_count
    }
    
    response = requests.post(website_url, json=payload)
    
    return response

def lambda_handler(event, context):
    is_valid, result = validate_input(event)
    if not is_valid:
        return {
            'statusCode': 400,
            'body': json.dumps(result)
        }
    
    company_name, interview_date = result

    data_points = get_metric_statistics(company_name, interview_date)
    if not data_points:
        return {
            'statusCode': 200,
            'body': json.dumps('No data points found for the specified time range.')
        }
    
    for data_point in data_points:
        interview_count = data_point['Sum']
        if not company_name:
            company_name = 'Unknown'
        if not interview_date:
            interview_date = 'Unknown'

        response = send_metric_to_website(company_name, interview_date, interview_count)
        
        if response.status_code != 200:
            return {
                'statusCode': response.status_code,
                'body': json.dumps('Failed to send metric data to the website.')
            }
    
    return {
        'statusCode': 200,
        'body': json.dumps('Metric data successfully sent to the website.')
    }