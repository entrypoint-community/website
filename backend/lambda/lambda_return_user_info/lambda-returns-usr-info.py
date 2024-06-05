from lambdaRetrieveDataLibrary.lambda_return_data import lambda_handler, check_table
import json

secret_Name = "secretName"
event = {}
context = {}
table = "users"

table_exist = check_table(table)

if table_exist:
    data = lambda_handler(event, context, table)
    data_json = json.dumps(data)