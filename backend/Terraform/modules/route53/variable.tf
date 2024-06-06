variable "route53_domain_name" {
  description = "The domain name for the hosted zone"
  type        = string
  default     = "www.entrypoint" # change to the real DNS name 
}

variable "route53_record_name" {
  type        = string
  description = "name of the record"
  default     = "surfsupsnir.com"
}