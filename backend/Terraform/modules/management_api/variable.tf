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
    announcement = {
      path = "announcement_lambda"
      http_method = "POST"
      method_response_status_code = "200"
    }
    blog_post = {
      path = "blog_post_lambda"
      http_method = "POST"
      method_response_status_code = "200"
    }
    drive_contects = {
      path = "drive_contects"
      http_method = "POST"
      method_response_status_code = "200"
    }
    community_statistics = {
      path = "community_statistics"
      http_method = "POST"
      method_response_status_code = "200"
    }
    community_members = {
      path = "community_members"
      http_method = "POST"
      method_response_status_code = "200"
    }
    registration_form = {
      path = "registration_form"
      http_method = "POST"
      method_response_status_code = "200"
    }
    community_blog_posts = {
      path = "community_blog_posts"
      http_method = "POST"
      method_response_status_code = "200"
    }
  }
}
