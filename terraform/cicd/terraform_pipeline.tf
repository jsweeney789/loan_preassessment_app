resource "aws_codebuild_project" "terraform" {
  name          = "${var.environment}-terraform-build"
  description   = "Run terraform plan + apply for the dev environment"
  service_role  = aws_iam_role.codebuild_terraform.arn
  build_timeout = 60

  artifacts {
    type = "CODEPIPELINE"
  }

  environment {
    compute_type    = "BUILD_GENERAL1_SMALL"
    image           = "aws/codebuild/standard:7.0"
    type            = "LINUX_CONTAINER"
    privileged_mode = false

    environment_variable {
      name  = "TF_VERSION"
      value = var.terraform_version
    }
    environment_variable {
      name  = "TF_DIR"
      value = "terraform/environments/${var.environment}"
    }
  }

  source {
    type      = "CODEPIPELINE"
    buildspec = <<-YAML
      version: 0.2
      phases:
        install:
          commands:
            - curl -sSLo /tmp/terraform.zip https://releases.hashicorp.com/terraform/$TF_VERSION/terraform_$${TF_VERSION}_linux_amd64.zip
            - unzip -q /tmp/terraform.zip -d /usr/local/bin
            - terraform version
        pre_build:
          commands:
            - cd $TF_DIR && terraform init -input=false
        build:
          commands:
            - terraform plan -input=false -out=tfplan
        post_build:
          commands:
            - terraform apply -auto-approve tfplan
    YAML
  }

  logs_config {
    cloudwatch_logs {
      group_name  = "/codebuild/${var.environment}-terraform-build"
      stream_name = "build"
    }
  }

  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_codepipeline" "terraform" {
  name           = "${var.environment}-terraform-pipeline"
  role_arn       = aws_iam_role.codepipeline.arn
  pipeline_type  = "V2"
  execution_mode = "QUEUED" # queue infra changes — never supersede in-progress applies

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
    name = "Apply"
    action {
      name            = "TerraformApply"
      category        = "Build"
      owner           = "AWS"
      provider        = "CodeBuild"
      version         = "1"
      input_artifacts = ["source"]
      configuration = {
        ProjectName = aws_codebuild_project.terraform.name
      }
    }
  }

  # Only triggers when terraform files change
  trigger {
    provider_type = "CodeStarSourceConnection"
    git_configuration {
      source_action_name = "Source"
      push {
        branches { includes = [var.deploy_branch] }
        file_paths { includes = ["terraform/**"] }
      }
    }
  }

  tags = merge(var.tags, { Environment = var.environment })
}
