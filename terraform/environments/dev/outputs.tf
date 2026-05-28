# For testing purposes

output "alb_dns_name" {
  description = "Hit this URL to reach the app"
  value       = module.app.alb_dns_name
}

output "ecr_repository_url" {
  description = "Push your Docker image here before deploying"
  value       = module.app.ecr_repository_url
}

output "ecs_cluster_name" {
  value = module.app.ecs_cluster_name
}

output "ecs_service_name" {
  value = module.app.ecs_service_name
}

output "cloudwatch_log_group" {
  value = module.app.cloudwatch_log_group
}

output "cloudfront_domain_name" {
  description = "Frontend URL"
  value       = module.frontend.cloudfront_domain_name
}

output "cloudfront_distribution_id" {
  description = "Used by CI/CD to invalidate the cache after a deploy"
  value       = module.frontend.cloudfront_distribution_id
}

output "s3_bucket_name" {
  description = "Used by CI/CD to sync Angular build artifacts"
  value       = module.frontend.s3_bucket_name
}

output "model_artifact_bucket" {
  description = "Upload trained model.tar.gz here before deploying the endpoint"
  value       = module.sagemaker.model_artifact_bucket
}

output "sagemaker_execution_role_arn" {
  description = "Pass to SageMaker training jobs"
  value       = module.sagemaker.sagemaker_execution_role_arn
}

# output "sagemaker_endpoint_name" {
#   description = "Endpoint name the ECS app calls via boto3"
#   value       = module.sagemaker.endpoint_name
# }
