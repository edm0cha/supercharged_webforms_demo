# data "archive_file" "requierements" {
#   type        = "zip"
#   source_dir  = "${path.root}/../backend/layers/requirements"
#   output_path = "requirements.zip"
# }

# data "archive_file" "langchain" {
#   type        = "zip"
#   source_dir  = "${path.root}/../backend/layers/requirements-langchain"
#   output_path = "langchain.zip"
# }


# resource "aws_lambda_layer_version" "requirements" {
#   filename            = data.archive_file.requierements.output_path
#   layer_name          = "${var.function_name}-requirements"
#   compatible_runtimes = ["python3.11", "python3.12"]
#   source_code_hash    = data.archive_file.requierements.output_base64sha256
# }

# resource "aws_lambda_layer_version" "langchain1" {
#   filename            = "${path.root}/python.zip"
#   layer_name          = "${var.function_name}-langchain"
#   compatible_runtimes = ["python3.11", "python3.12"]
# }
