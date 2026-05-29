# ── Artifact Bucket ───────────────────────────────────────────────────────────
# Shared across all three pipelines for input/output artifacts

resource "aws_s3_bucket" "artifacts" {
  bucket        = "${var.project_name}-pipeline-artifacts"
  force_destroy = true

  tags = merge(var.tags, {
    Name        = "${var.project_name}-pipeline-artifacts"
    Environment = var.environment
  })
}

resource "aws_s3_bucket_versioning" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  rule {
    apply_server_side_encryption_by_default { sse_algorithm = "AES256" }
  }
}

resource "aws_s3_bucket_public_access_block" "artifacts" {
  bucket                  = aws_s3_bucket.artifacts.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "artifacts" {
  bucket = aws_s3_bucket.artifacts.id
  rule {
    id     = "expire-old-artifacts"
    status = "Enabled"
    filter {}
    expiration { days = 30 }
  }
}

# ── CodeCommit Repository ─────────────────────────────────────────────────────

resource "aws_codecommit_repository" "app" {
  repository_name = var.codecommit_repo_name
  description     = "Source repository for ${var.project_name}"

  tags = merge(var.tags, {
    Name        = var.codecommit_repo_name
    Environment = var.environment
  })
}
