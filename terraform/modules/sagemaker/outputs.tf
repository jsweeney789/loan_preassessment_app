output "model_artifact_bucket" {
  description = "S3 bucket where CI/CD uploads trained model artifacts"
  value       = var.training_data_bucket_arn
}

output "model_artifact_bucket_arn" {
  description = "ARN of the model artifact bucket"
  value       = var.training_data_bucket_arn
}

output "sagemaker_execution_role_arn" {
  description = "IAM role ARN assumed by SageMaker — pass to training jobs and model registry"
  value       = aws_iam_role.sagemaker_execution.arn
}

# output "endpoint_name" {
#   description = "SageMaker endpoint name the ECS app calls. Empty until model_artifact_s3_uri is set."
#   value       = local.deploy_endpoint ? aws_sagemaker_endpoint.loan[0].name : ""
# }

# output "endpoint_arn" {
#   description = "SageMaker endpoint ARN. Empty until model_artifact_s3_uri is set."
#   value       = local.deploy_endpoint ? aws_sagemaker_endpoint.loan[0].arn : ""
# }