output "github_connection_arn" {
  description = "Activate this connection in the AWS Console before the pipelines can trigger: Developer Tools → Connections"
  value       = aws_codestarconnections_connection.github.arn
}

output "github_connection_status" {
  description = "Must be AVAILABLE (not PENDING) before pipelines will trigger"
  value       = aws_codestarconnections_connection.github.connection_status
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
