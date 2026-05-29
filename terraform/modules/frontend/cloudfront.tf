# ── Origin Access Control ─────────────────────────────────────────────────────
# OAC is the modern replacement for OAI — signs requests to S3 with SigV4

resource "aws_cloudfront_origin_access_control" "frontend" {
  name                              = "${var.project_name}-frontend-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"


  lifecycle {
    create_before_destroy = true
  }
}

# ── CloudFront Distribution ───────────────────────────────────────────────────

resource "aws_cloudfront_distribution" "frontend" {
  enabled             = true
  default_root_object = "index.html"
  comment             = "${var.environment} loan pre-assessment frontend"

  # Restrict to US/EU in dev to save cost; use All in prod
  price_class = var.environment == "prod" ? "PriceClass_All" : "PriceClass_100"

  origin {
    domain_name              = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id                = "S3-${aws_s3_bucket.frontend.id}"
    origin_access_control_id = aws_cloudfront_origin_access_control.frontend.id
  }

  origin {
    domain_name = var.alb_dns_name
    origin_id   = "ALB-${var.alb_dns_name}"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  # ── /api/* → ALB (proxied over HTTPS from browser, HTTP to ALB internally) ──
  ordered_cache_behavior {
    path_pattern           = "/api/*"
    target_origin_id       = "ALB-${var.alb_dns_name}"
    viewer_protocol_policy = "https-only"
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    compress               = true

    cache_policy_id          = "4135ea2d-6df8-44a3-9df3-4b5a84be39ad" # CachingDisabled
    origin_request_policy_id = "b689b0a8-53d0-40ab-baf2-68738e2966ac" # AllViewerExceptHostHeader
  }

  # ── Default cache behaviour (all paths) ──────────────────────────────────────
  default_cache_behavior {
    target_origin_id       = "S3-${aws_s3_bucket.frontend.id}"
    viewer_protocol_policy = "redirect-to-https"
    compress               = true
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]

    # AWS managed CachingOptimized policy
    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"
  }

  # ── Angular HTML5 routing ─────────────────────────────────────────────────────
  # S3 returns 403 (not 404) for missing keys when the bucket is private.
  # Both are mapped to index.html so the Angular router can take over.
  custom_error_response {
    error_code            = 403
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 0
  }

  custom_error_response {
    error_code            = 404
    response_code         = 200
    response_page_path    = "/index.html"
    error_caching_min_ttl = 0
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  # Default CloudFront certificate (*.cloudfront.net)
  # Replace with acm_certificate_arn + aliases once you have a custom domain
  viewer_certificate {
    cloudfront_default_certificate = true
  }

  tags = merge(var.tags, {
    Name        = "${var.project_name}-frontend-cdn"
    Environment = var.environment
  })
}
