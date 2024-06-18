variable "api_name" {
  description = "The name for the api"
  type        = string
  default     = "management_api"
}

variable "api_deployment_name" {
  type        = string
  description = "The name of the API Gateway deployment"
  default     = "dev"
}

variable "lambda_paths" {
  description = "Map of Lambda function paths with http_method and method_response_status_code"
  type = map(object({
    path                      = string
    http_method               = string
    method_response_status_code = string
  }))
  default = {
 
  }
}
