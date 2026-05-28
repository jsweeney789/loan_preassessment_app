data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# ── CodePipeline Role ─────────────────────────────────────────────────────────

resource "aws_iam_role" "codepipeline" {
  name = "${var.environment}-codepipeline-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "codepipeline.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_iam_role_policy" "codepipeline" {
  name = "${var.environment}-codepipeline-policy"
  role = aws_iam_role.codepipeline.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "ArtifactBucket"
        Effect = "Allow"
        Action = ["s3:GetObject", "s3:PutObject", "s3:GetBucketVersioning", "s3:ListBucket"]
        Resource = [
          aws_s3_bucket.artifacts.arn,
          "${aws_s3_bucket.artifacts.arn}/*"
        ]
      },
      {
        Sid      = "CodeBuild"
        Effect   = "Allow"
        Action   = ["codebuild:BatchGetBuilds", "codebuild:StartBuild"]
        Resource = "*"
      },
      {
        Sid      = "GitHubConnection"
        Effect   = "Allow"
        Action   = ["codestar-connections:UseConnection"]
        Resource = local.github_connection_arn
      },
      {
        Sid      = "PassRole"
        Effect   = "Allow"
        Action   = ["iam:PassRole"]
        Resource = "*"
        Condition = {
          StringEqualsIfExists = {
            "iam:PassedToService" = ["codebuild.amazonaws.com"]
          }
        }
      }
    ]
  })
}

# ── CodeBuild Role — Backend ──────────────────────────────────────────────────

resource "aws_iam_role" "codebuild_backend" {
  name = "${var.environment}-codebuild-backend-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "codebuild.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_iam_role_policy" "codebuild_backend" {
  name = "${var.environment}-codebuild-backend-policy"
  role = aws_iam_role.codebuild_backend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "ECRAuth"
        Effect   = "Allow"
        Action   = ["ecr:GetAuthorizationToken"]
        Resource = "*"
      },
      {
        Sid    = "ECRPush"
        Effect = "Allow"
        Action = [
          "ecr:BatchCheckLayerAvailability", "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage", "ecr:PutImage", "ecr:InitiateLayerUpload",
          "ecr:UploadLayerPart", "ecr:CompleteLayerUpload"
        ]
        Resource = "arn:aws:ecr:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:repository/${var.environment}-*"
      },
      {
        Sid      = "ECSUpdate"
        Effect   = "Allow"
        Action   = ["ecs:UpdateService", "ecs:DescribeServices", "ecs:RegisterTaskDefinition", "ecs:DescribeTaskDefinition"]
        Resource = "*"
      },
      {
        Sid    = "ArtifactBucket"
        Effect = "Allow"
        Action = ["s3:GetObject", "s3:PutObject", "s3:GetBucketVersioning"]
        Resource = [aws_s3_bucket.artifacts.arn, "${aws_s3_bucket.artifacts.arn}/*"]
      },
      {
        Sid      = "Logs"
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/codebuild/*"
      }
    ]
  })
}

# ── CodeBuild Role — Frontend ─────────────────────────────────────────────────

resource "aws_iam_role" "codebuild_frontend" {
  name = "${var.environment}-codebuild-frontend-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "codebuild.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_iam_role_policy" "codebuild_frontend" {
  name = "${var.environment}-codebuild-frontend-policy"
  role = aws_iam_role.codebuild_frontend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "FrontendBucket"
        Effect = "Allow"
        Action = ["s3:PutObject", "s3:DeleteObject", "s3:GetObject", "s3:ListBucket"]
        Resource = [
          "arn:aws:s3:::${var.frontend_bucket_name}",
          "arn:aws:s3:::${var.frontend_bucket_name}/*"
        ]
      },
      {
        Sid      = "CloudFrontInvalidate"
        Effect   = "Allow"
        Action   = ["cloudfront:CreateInvalidation"]
        Resource = "arn:aws:cloudfront::${data.aws_caller_identity.current.account_id}:distribution/${var.cloudfront_distribution_id}"
      },
      {
        Sid    = "ArtifactBucket"
        Effect = "Allow"
        Action = ["s3:GetObject", "s3:PutObject", "s3:GetBucketVersioning"]
        Resource = [aws_s3_bucket.artifacts.arn, "${aws_s3_bucket.artifacts.arn}/*"]
      },
      {
        Sid      = "Logs"
        Effect   = "Allow"
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"]
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/codebuild/*"
      }
    ]
  })
}

# ── CodeBuild Role — Terraform ────────────────────────────────────────────────
# Broad inline policy — Terraform creates/destroys arbitrary resources.
# Inline avoids iam:AttachRolePolicy (which SSO Java-Full-Stack lacks).
# Scope this down once the infrastructure stabilizes.

resource "aws_iam_role" "codebuild_terraform" {
  name = "${var.environment}-codebuild-terraform-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "codebuild.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })

  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_iam_role_policy" "codebuild_terraform_admin" {
  name = "${var.environment}-codebuild-terraform-policy"
  role = aws_iam_role.codebuild_terraform.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid      = "Admin"
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}
