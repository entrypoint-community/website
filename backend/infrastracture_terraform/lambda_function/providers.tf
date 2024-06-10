terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

#in order to auth with aws and enables to interact with the cloud in a declarative way
provider "aws" {
  region = variable.region
}
