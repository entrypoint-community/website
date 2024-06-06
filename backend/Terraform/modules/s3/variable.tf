variable "s3_bucket_name" {
  type        = string
  description = "the name of the bucket"
  default     = "website_entryPoint"
}

variable "s3_bucket_website_index_document" {
  type        = string
  description = "the default file for the static website"
  default     = "index.html" #change to the real index.html
}