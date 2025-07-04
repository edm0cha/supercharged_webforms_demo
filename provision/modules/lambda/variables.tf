variable "function_name" {
  type        = string
  description = "Unique name for your Lambda Function"
}

variable "source_file" {
  type        = string
  description = "Path to the source code of your Lambda Function"
}

variable "handler" {
  type        = string
  description = "Function entrypoint in your code."
  default     = "lambda.lambda_handler"
}

variable "runtime" {
  type        = string
  description = "Identifier of the function's runtime"
  default     = "python3.12"
}

variable "timeout" {
  type        = number
  description = "How long can run before throwing a timeout erorr"
  default     = 80
}

variable "memory_size" {
  type        = number
  description = "The memory size of the machine running the function"
  default     = 256
}

variable "dynamo_table_name" {
  type        = string
  description = "The name of the DynamoDB table"
}

variable "dynamo_table_arn" {
  type        = string
  description = "The arn of the DynamoDB table"
}

variable "endpoint_allowed_methods" {
  type        = list(string)
  description = "Allowed HTTP methods for the API Gateway endpoint"
  default     = ["POST"]
}
