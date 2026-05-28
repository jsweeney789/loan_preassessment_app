output "github_connection_arn" {
  description = "Activate this connection in the AWS Console before the pipelines can trigger: Developer Tools → Connections"
  value       = local.github_connection_arn
}

output "github_connection_status" {
  description = "Must be AVAILABLE (not PENDING) before pipelines will trigger"
  value       = var.existing_github_connection_arn == "" ? aws_codestarconnections_connection.github[0].connection_status : "AVAILABLE"
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
