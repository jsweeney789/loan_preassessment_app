# ── S3 Bucket ─────────────────────────────────────────────────────────────────
# Not publicly accessible — CloudFront is the only allowed reader via OAC

resource "aws_s3_bucket" "frontend" {
  bucket = "${var.project_name}-frontend"

  tags = merge(var.tags, {
    Name        = "${var.project_name}-frontend"
    Environment = var.environment
  })
}

resource "aws_s3_bucket_versioning" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Block all direct public access — CloudFront OAC handles reads
resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ── Bucket Policy — only CloudFront (via OAC) can read objects ────────────────

data "aws_iam_policy_document" "cloudfront_read" {
  statement {
    sid    = "AllowCloudFrontOAC"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.frontend.arn}/*"]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.frontend.arn]
    }
  }
}

resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id
  policy = data.aws_iam_policy_document.cloudfront_read.json

  # Policy references the distribution ARN, so the distribution must exist first
  depends_on = [aws_cloudfront_distribution.frontend]
}
