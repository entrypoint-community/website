from lambdaretrievedatalibrary.lambda_return_data import lambda_handler
import json

event = {}
context = {}
table = "blog_posting"

data = lambda_handler(event, context, table)
    
data_json = json.dumps(data)