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
    environment_variable {
      name  = "EKS_CLUSTER"
      value = var.eks_cluster_name
    }
    environment_variable {
      name  = "EKS_NAMESPACE"
      value = var.eks_namespace
    }
    environment_variable {
      name  = "DB_SECRET_ARN"
      value = var.db_secret_arn
    }
    environment_variable {
      name  = "GOOGLE_OAUTH_SECRET_ARN"
      value = var.google_oauth_secret_arn
    }
    environment_variable {
      name  = "AUTH_SECRET_ARN"
      value = var.auth_secret_arn
    }
    environment_variable {
      name  = "CORS_ORIGIN"
      value = var.cors_origin
    }
    environment_variable {
      name  = "GOOGLE_CLIENT_ID"
      value = var.google_client_id
    }
    environment_variable {
      name  = "GOOGLE_REDIRECT_URI"
      value = var.google_redirect_uri
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
            - aws eks update-kubeconfig --name $EKS_CLUSTER --region $AWS_DEFAULT_REGION
            - kubectl create namespace $EKS_NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
            - |
              DB=$(aws secretsmanager get-secret-value --secret-id $DB_SECRET_ARN --query SecretString --output text)
              GO=$(aws secretsmanager get-secret-value --secret-id $GOOGLE_OAUTH_SECRET_ARN --query SecretString --output text)
              AU=$(aws secretsmanager get-secret-value --secret-id $AUTH_SECRET_ARN --query SecretString --output text)
              kubectl create secret generic loan-preassessment-secrets \
                --namespace=$EKS_NAMESPACE \
                --from-literal=DB_HOST=$(echo $DB | python3 -c "import sys,json; print(json.load(sys.stdin)['host'])") \
                --from-literal=DB_PORT=$(echo $DB | python3 -c "import sys,json; print(json.load(sys.stdin)['port'])") \
                --from-literal=DB_NAME=$(echo $DB | python3 -c "import sys,json; print(json.load(sys.stdin)['dbname'])") \
                --from-literal=DB_USERNAME=$(echo $DB | python3 -c "import sys,json; print(json.load(sys.stdin)['username'])") \
                --from-literal=DB_PASSWORD=$(echo $DB | python3 -c "import sys,json; print(json.load(sys.stdin)['password'])") \
                --from-literal=GOOGLE_CLIENT_SECRET=$(echo $GO | python3 -c "import sys,json; print(json.load(sys.stdin)['client_secret'])") \
                --from-literal=JWT_SECRET=$(echo $AU | python3 -c "import sys,json; print(json.load(sys.stdin)['jwt_secret'])") \
                --from-literal=SESSION_SECRET=$(echo $AU | python3 -c "import sys,json; print(json.load(sys.stdin)['session_secret'])") \
                --dry-run=client -o yaml | kubectl apply -f -
            - |
              kubectl create configmap loan-preassessment-config \
                --namespace=$EKS_NAMESPACE \
                --from-literal=ENVIRONMENT=$ENVIRONMENT \
                --from-literal=PORT=8000 \
                --from-literal=CORS_ORIGIN=$CORS_ORIGIN \
                --from-literal=GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID \
                --from-literal=GOOGLE_REDIRECT_URI=$GOOGLE_REDIRECT_URI \
                --dry-run=client -o yaml | kubectl apply -f -
            - kubectl apply -f k8s/namespace.yaml
            - kubectl apply -f k8s/service.yaml
            - kubectl apply -f k8s/ingress.yaml
            - sed "s|ECR_PLACEHOLDER|$ECR_REPO_URL:$CODEBUILD_RESOLVED_SOURCE_VERSION|g" k8s/deployment.yaml | kubectl apply -f -
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
