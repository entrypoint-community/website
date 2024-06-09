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