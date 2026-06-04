output "codecommit_clone_url_http" {
  description = "HTTPS clone URL — use this to push code to CodeCommit"
  value       = aws_codecommit_repository.app.clone_url_http
}

output "codecommit_clone_url_ssh" {
  description = "SSH clone URL for CodeCommit"
  value       = aws_codecommit_repository.app.clone_url_ssh
}

output "backend_pipeline_name" {
  value = aws_codepipeline.backend.name
}

output "frontend_pipeline_name" {
  value = aws_codepipeline.frontend.name
}

output "terraform_pipeline_name" {
  value = aws_codepipeline.terraform.name
}

output "codebuild_backend_role_arn" {
  description = "ARN of the CodeBuild backend role — used to grant it EKS cluster access"
  value       = aws_iam_role.codebuild_backend.arn
}
