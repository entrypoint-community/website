resource "aws_api_gateway_rest_api" "management_api" {
  name = var.api_name
  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "lambda_resource" {
  for_each    = var.lambda_paths
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  parent_id   = aws_api_gateway_rest_api.management_api.root_resource_id
  path_part   = each.value
}

resource "aws_api_gateway_method" "lambda_method" {
  for_each      = aws_api_gateway_resource.lambda_resource
  rest_api_id   = aws_api_gateway_rest_api.management_api.id
  resource_id   = each.value.id
  http_method   = var.http_method
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  for_each                = aws_api_gateway_resource.lambda_resource
  rest_api_id             = aws_api_gateway_rest_api.management_api.id
  resource_id             = each.value.id
  http_method             = aws_api_gateway_method.lambda_method[each.key].http_method
  integration_http_method = var.http_method
  type                    = "AWS"
  uri                     = aws_lambda_function[each.key].invoke_arn
}

resource "aws_api_gateway_method_response" "lambda_method_response" {
  for_each      = aws_api_gateway_resource.lambda_resource
  rest_api_id   = aws_api_gateway_rest_api.management_api.id
  resource_id   = each.value.id
  http_method   = aws_api_gateway_method.lambda_method[each.key].http_method
  status_code   = var.method_response_status_code
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true,
    "method.response.header.Access-Control-Allow-Methods" = true,
    "method.response.header.Access-Control-Allow-Origin" = true
  }
}

resource "aws_api_gateway_integration_response" "lambda_integration_response" {
  for_each      = aws_api_gateway_resource.lambda_resource
  rest_api_id   = aws_api_gateway_rest_api.management_api.id
  resource_id   = each.value.id
  http_method   = aws_api_gateway_method.lambda_method[each.key].http_method
  status_code   = aws_api_gateway_method_response.lambda_method_response[each.key].status_code
  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,Content-Length,DateX-Amz-Apigw-Id,X-Amzn-Errortype,X-Amzn-Requestid '",
    "method.response.header.Access-Control-Allow-Methods" = "'GET,OPTIONS,POST,PUT'",
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }
  depends_on = [
    aws_api_gateway_integration.lambda_integration
  ]
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.management_api.id
  stage_name  = var.api_deployment_name
  depends_on  = [aws_api_gateway_integration.lambda_integration]
}

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
  role       = aws_iam_role.iam_for_lambda.name
}

resource "aws_lambda_permission" "apigw_lambda" {
  for_each     = aws_api_gateway_resource.lambda_resource
  statement_id = "AllowExecutionFromAPIGateway"
  action       = "lambda:InvokeFunction"
  function_name = aws_lambda_function[each.key].function_name
  principal    = "apigateway.amazonaws.com"
  source_arn   = "${aws_api_gateway_rest_api.management_api.execution_arn}/*/*/*"
}