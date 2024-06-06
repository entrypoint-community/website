resource "aws_route53_zone" "website" {
  name = var.route53_domain_name
}

resource "aws_route53_record" "example" {
  zone_id = aws_route53_zone.website.zone_id
  name    = var.route53_record_name
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.cloudfront_dist.domain_name
    zone_id                = aws_cloudfront_distribution.cloudfront_dist.hosted_zone_id
    evaluate_target_health = true
  }
}