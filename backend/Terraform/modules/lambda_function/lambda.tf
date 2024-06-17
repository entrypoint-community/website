data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "iam_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

data "archive_file" "lambda" {
  type        = var.archive_type
  source_file = var.source_file
  output_path = var.output_path
}

resource "aws_lambda_function" "gda_lambda" {
  filename      = var.output_path
  function_name = var.function_name
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = var.handler
  source_code_hash = data.archive_file.lambda.output_base64sha256
  runtime       = var.runtime

  environment {
    variables = var.environment_variables
  }
}
