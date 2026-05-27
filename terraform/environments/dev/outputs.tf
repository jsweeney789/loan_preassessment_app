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
