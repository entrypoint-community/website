variable "region" {
  description = "The AWS region to deploy to"
  default     = "us-east-1"
  type        = string
}

variable "s3_bucket" {
  description = "The S3 bucket containing the Lambda function code"
  default     = "entrypoint_bucket"
  type        = string
}

variable "s3_key" {
  description = "The S3 key for the Lambda function code"
  default     = ""
  type        = string
}

variable "function_name" {
  description = "The name of the Lambda function"
  type        = string
}

variable "handler" {
  description = "The function handler for the Lambda function"
  type        = string
}

variable "runtime" {
  description = "The runtime environment for the Lambda function"
  default     = "python3.9"
  type        = string
}

variable "archive_type" {
  description = "The type of the archive file"
  type        = string
  default     = "zip"
}

variable "source_file" {
  description = "The source file for the Lambda function"
  type        = string
}

variable "output_path" {
  description = "The output path for the Lambda function archive"
  type        = string
}

variable "environment_variables" {
  description = "A map of environment variables for the Lambda function"
  type        = map(string)
  default     = {}
}
