from lambdaRetrieveDataLibrary.lambda_return_data import retrieve_data

def lambda_handler(event, context):
    data = retrieve_data(table_name="users")
    return data