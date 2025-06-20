data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "lambda_execution_role" {
  name               = var.function_name
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_policy" "cloudwatch" {
  name        = "${var.function_name}-cloudwatch"
  description = "Policy allowing Lambda to use different services"
  policy = templatefile("${path.module}/policies/cloudwatch.json", {
    cloudwatch_arn = aws_cloudwatch_log_group.this.arn
  })
}

resource "aws_iam_policy" "dynamodb" {
  name        = "${var.function_name}-dynamodb"
  description = "Policy allowing store and retrieve of DynamoDB"
  policy = templatefile("${path.module}/policies/dynamodb.json", {
    dynamodb_table_arn = var.dynamo_table_arn
  })
}

resource "aws_iam_policy" "bedrock" {
  name        = "${var.function_name}-bedrock"
  description = "Policy allowing store and invoke Bedrock model"
  policy      = templatefile("${path.module}/policies/bedrock.json", {})
}

resource "aws_iam_role_policy_attachment" "attach_logs_policy" {
  policy_arn = aws_iam_policy.cloudwatch.arn
  role       = aws_iam_role.lambda_execution_role.name
}

resource "aws_iam_role_policy_attachment" "attach_dynamodb_policy" {
  policy_arn = aws_iam_policy.dynamodb.arn
  role       = aws_iam_role.lambda_execution_role.name
}

resource "aws_iam_role_policy_attachment" "attach_bedrock_policy" {
  policy_arn = aws_iam_policy.bedrock.arn
  role       = aws_iam_role.lambda_execution_role.name
}
