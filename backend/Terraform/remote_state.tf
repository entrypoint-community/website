terraform {
  backend "s3" {
    bucket = "s3_backup" #we need to change this for the real s3 bucket
    key    = "backup/terraform.tfstate"
    region = "us-east-1"
  }
}