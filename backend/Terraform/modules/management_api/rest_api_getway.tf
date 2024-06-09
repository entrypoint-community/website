resource "aws_api_gateway_rest_api" "management_api" {
  name        = var.api_name
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "announcement_lambda" {
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  parent_id   = aws_api_gateway_rest_api.management_api.root_resource_id
  path_part   = "announcement_lambda"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  resource_id = aws_api_gateway_resource.announcement_lambda.id
  http_method = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  resource_id = aws_api_gateway_resource.announcement_lambda.id
  http_method = aws_api_gateway_method.proxy.http_method
  integration_http_method = "POST"
  type = "AWS"
  uri = aws_lambda_function.name_of_the_lambda.invoke_arn #change to the real name of the lambda
}

resource "aws_api_gateway_method_response" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  resource_id = aws_api_gateway_resource.announcement_lambda.id
  http_method = aws_api_gateway_method.proxy.http_method
  status_code = "200"

    //cors section
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin" = true
  }

}

resource "aws_api_gateway_integration_response" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  resource_id = aws_api_gateway_resource.announcement_lambda.id
  http_method = aws_api_gateway_method.proxy.http_method
  status_code = aws_api_gateway_method_response.proxy.status_code

    //cors
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" =  "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Content-Length,DateX-Amz-Apigw-Id,X-Amzn-Errortype,X-Amzn-Requestid '",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
}
  
  depends_on = [
    aws_api_gateway_method.proxy,
    aws_api_gateway_integration.lambda_integration
  ]
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  stage_name = var.api_deployment_name
  
  depends_on = [
    aws_api_gateway_integration.lambda_integration,
  ]
}

#if you we we will move this resource for the lambda module 
resource "aws_iam_role" "iam_for_lambda" {
  name = "lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
    {
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }
  ]
})
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role = aws_iam_role.iam_for_lambda.name
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id = "AllowExecutionFromAPIGateway"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.name_of_the_lambda.function_name #change to the real name of the lambda
  principal = "apigateway.amazonaws.com"
  source_arn = "${aws_api_gateway_rest_api.management_api.execution_arn}/*/*/*"
}

resource "aws_api_gateway_resource" "blog_post_lambda" {
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  parent_id   = aws_api_gateway_rest_api.management_api.root_resource_id
  path_part   = "blog_post_lambda"
}

resource "aws_api_gateway_method" "metric_lambda" {
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  resource_id = aws_api_gateway_resource.blog_post_lambda.id
  http_method = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "metric_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.management_api.id
  resource_id             = aws_api_gateway_resource.blog_post_lambda.id
  http_method             = aws_api_gateway_method.metric_lambda.http_method
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = aws_lambda_function.metric_lambda.invoke_arn #change to the real name of the lambda
}

resource "aws_api_gateway_method_response" "metric_lambda" {
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  resource_id = aws_api_gateway_resource.blog_post_lambda.id
  http_method = aws_api_gateway_method.metric_lambda.http_method
  status_code = "200"

    //cors section
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin" = true
  }

}

resource "aws_api_gateway_integration_response" "metric_lambda" {
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  resource_id = aws_api_gateway_resource.blog_post_lambda.id
  http_method = aws_api_gateway_method.metric_lambda.http_method
  status_code = aws_api_gateway_method_response.metric_lambda.status_code

    //cors
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" =  "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Content-Length,DateX-Amz-Apigw-Id,X-Amzn-Errortype,X-Amzn-Requestid '",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
}
  
  depends_on = [
    aws_api_gateway_method.metric_lambda,
    aws_api_gateway_integration.metric_lambda
  ]
}