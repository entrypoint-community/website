terraform {
  backend "s3" {
    bucket         = "entrypoint-state-bucket"
    key            = "lambda/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "entrypoint-table"
  }
}