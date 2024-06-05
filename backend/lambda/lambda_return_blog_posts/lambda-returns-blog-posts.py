from lambdaRetrieveDataLibrary.lambda_return_data import lambda_handler, check_table
import json

event = {}
context = {}
table = "blog_posting"

table_exist = check_table(table)

if table_exist:
    data = lambda_handler(event, context, table)
    data_json = json.dumps(data)