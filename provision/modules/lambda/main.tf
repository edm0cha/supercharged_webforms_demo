data "archive_file" "lambda" {
  type        = "zip"
  source_file = var.source_file
  output_path = "${var.function_name}.zip"
}

resource "aws_lambda_function" "this" {
  filename      = data.archive_file.lambda.output_path
  function_name = var.function_name
  role          = aws_iam_role.lambda_execution_role.arn
  handler       = var.handler
  runtime       = var.runtime
  timeout       = var.timeout
  layers = [
    "arn:aws:lambda:us-east-1:131578276461:layer:genai-langchain-genai-catalyst-hackathon:3"
  ]
  source_code_hash = data.archive_file.lambda.output_base64sha256
  memory_size      = var.memory_size
  environment {
    variables = {
      DYNAMO_TABLE_NAME = var.dynamo_table_name
    }
  }
}

resource "aws_lambda_function_url" "this" {
  function_name      = aws_lambda_function.this.function_name
  authorization_type = "NONE"

  cors {
    allow_origins = ["*"]
    allow_methods = var.endpoint_allowed_methods
    allow_headers = ["*"]
    max_age       = 86400
  }
}

resource "aws_cloudwatch_log_group" "this" {
  name = "/aws/lambda/${var.function_name}"
}
