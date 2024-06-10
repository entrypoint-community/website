variable "api_name" {
  description = "The name for the api"
  type        = string
  default     = "management_api" 
}

variable "api_deployment_name" {
    type = string
    description = "the name of the api gateway deployment"
    default = "dev"
}

variable "lambda_paths" {
  description = "Map of Lambda function paths"
  type        = map(string)
  default     = {
    announcement = "announcement_lambda"
    blog_post    = "blog_post_lambda"
    drive_contects = "drive_contects"
    community_statistics = "community_statistics"
    community_members = "community_members"
    registration_form = "registration_form"
    community_blog_posts = "community_blog_posts"
  }
}

variable "http_method" {
    type = string
    description = "http_method"
    default = "POST"
}

variable "method_response_status_code" {
    type = string
    description = "method response status code"
    default = "200"
}