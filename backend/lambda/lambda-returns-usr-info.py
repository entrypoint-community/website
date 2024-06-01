from lambdaretrievedatalibrary.lambda_return_data import lambda_handler
import json

secret_Name = "secretName"
event = {}
context = {}
table = "users"

data = lambda_handler(event, context, table)
    
data_json = json.dumps(data)