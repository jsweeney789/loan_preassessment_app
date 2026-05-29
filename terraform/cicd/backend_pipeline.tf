resource "aws_codebuild_project" "backend" {
  name          = "${var.environment}-backend-build"
  description   = "Build and push backend Docker image, force new ECS deployment"
  service_role  = aws_iam_role.codebuild_backend.arn
  build_timeout = 20

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type    = "BUILD_GENERAL1_SMALL"
    image           = "aws/codebuild/standard:7.0"
    type            = "LINUX_CONTAINER"
    privileged_mode = true # required for Docker builds

    environment_variable {
      name  = "ECR_REPO_URL"
      value = var.ecr_repository_url
    }
    environment_variable {
      name  = "ECS_CLUSTER"
      value = var.ecs_cluster_name
    }
    environment_variable {
      name  = "ECS_SERVICE"
      value = var.ecs_service_name
    }
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = <<-YAML
      version: 0.2
      phases:
        pre_build:
          commands:
            - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $ECR_REPO_URL
        build:
          commands:
            - docker build -f backendLoanAssessment/Dockerfile -t $ECR_REPO_URL:$CODEBUILD_RESOLVED_SOURCE_VERSION .
            - docker tag $ECR_REPO_URL:$CODEBUILD_RESOLVED_SOURCE_VERSION $ECR_REPO_URL:latest
        post_build:
          commands:
            - docker push $ECR_REPO_URL:$CODEBUILD_RESOLVED_SOURCE_VERSION
            - docker push $ECR_REPO_URL:latest
            - aws ecs update-service --cluster $ECS_CLUSTER --service $ECS_SERVICE --force-new-deployment --region $AWS_DEFAULT_REGION
    YAML
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "/codebuild/${var.environment}-backend-build"
      stream_name = "build"
    }
  }

  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_codepipeline" "backend" {
  name           = "${var.environment}-backend-pipeline"
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
      provider         = "CodeCommit"
      version          = "1"
      output_artifacts = ["source"]
      configuration = {
        RepositoryName       = var.codecommit_repo_name
        BranchName           = var.deploy_branch
        PollForSourceChanges = "true"
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
        ProjectName = aws_codebuild_project.backend.name
      }
    }
  }

  tags = merge(var.tags, { Environment = var.environment })
}
