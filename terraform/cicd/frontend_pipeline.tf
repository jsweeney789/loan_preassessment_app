resource "aws_codebuild_project" "frontend" {
  name          = "${var.environment}-frontend-build"
  description   = "Build Angular app and deploy to S3 + CloudFront"
  service_role  = aws_iam_role.codebuild_frontend.arn
  build_timeout = 15

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type    = "BUILD_GENERAL1_SMALL"
    image           = "aws/codebuild/standard:7.0"
    type            = "LINUX_CONTAINER"
    privileged_mode = false

    environment_variable {
      name  = "FRONTEND_BUCKET"
      value = var.frontend_bucket_name
    }
    environment_variable {
      name  = "CLOUDFRONT_DIST_ID"
      value = var.cloudfront_distribution_id
    }
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = <<-YAML
      version: 0.2
      phases:
        install:
          runtime-versions:
            nodejs: 20
          commands:
            - cd frontend-loan-assessment && npm ci
        build:
          commands:
            - cd frontend-loan-assessment && npm run build -- --configuration production
        post_build:
          commands:
            - aws s3 sync frontend-loan-assessment/dist/frontend-loan-assessment/browser/ s3://$FRONTEND_BUCKET --delete
            - aws s3 cp frontend-loan-assessment/dist/frontend-loan-assessment/browser/index.html s3://$FRONTEND_BUCKET/index.html --cache-control "no-cache, no-store, must-revalidate" --content-type "text/html"
            - aws cloudfront create-invalidation --distribution-id $CLOUDFRONT_DIST_ID --paths "/*"
    YAML
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "/codebuild/${var.environment}-frontend-build"
      stream_name = "build"
    }
  }

  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_codepipeline" "frontend" {
  name           = "${var.environment}-frontend-pipeline"
  role_arn       = aws_iam_role.codepipeline.arn
  pipeline_type  = "V2"
  execution_mode = "SUPERSEDED"

  artifact_store {
    location = aws_s3_bucket.artifacts.bucket
    type     = "S3"
  }

  stage {
    name = "Source"
    action {
      name             = "Source"
      category         = "Source"
      owner            = "AWS"
      provider         = "CodeStarSourceConnection"
      version          = "1"
      output_artifacts = ["source"]
      configuration = {
        ConnectionArn        = local.github_connection_arn
        FullRepositoryId     = "${var.github_owner}/${var.github_repo}"
        BranchName           = var.deploy_branch
        OutputArtifactFormat = "CODE_ZIP"
      }
    }
  }

  stage {
    name = "Build"
    action {
      name            = "BuildAndDeploy"
      category        = "Build"
      owner           = "AWS"
      provider        = "CodeBuild"
      version         = "1"
      input_artifacts = ["source"]
      configuration = {
        ProjectName = aws_codebuild_project.frontend.name
      }
    }
  }

  # Only triggers when frontend-related files change
  trigger {
    provider_type = "CodeStarSourceConnection"
    git_configuration {
      source_action_name = "Source"
      push {
        branches { includes = [var.deploy_branch] }
        file_paths { includes = ["frontend-loan-assessment/**"] }
      }
    }
  }

  tags = merge(var.tags, { Environment = var.environment })
}
