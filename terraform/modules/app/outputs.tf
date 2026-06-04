output "ecs_task_execution_role_arn" {
  description = "ARN of the ECS task execution role (used by the ECS agent)"
  value       = aws_iam_role.ecs_task_execution.arn
}

output "ecs_task_role_arn" {
  description = "ARN of the ECS task role (used by the application at runtime)"
  value       = aws_iam_role.ecs_task.arn
}

output "ecr_repository_url" {
  description = "ECR repository URL — push images here before deploying"
  value       = aws_ecr_repository.app.repository_url
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = aws_lb.app.dns_name
}

output "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  value       = aws_ecs_cluster.main.name
}

output "ecs_service_name" {
  description = "Name of the ECS service"
  value       = aws_ecs_service.app.name
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group name for the application"
  value       = aws_cloudwatch_log_group.app.name
}

output "google_oauth_secret_arn" {
  description = "ARN of the Google OAuth secret in Secrets Manager"
  value       = aws_secretsmanager_secret.google_oauth.arn
}

output "auth_secret_arn" {
  description = "ARN of the JWT/session auth secret in Secrets Manager"
  value       = aws_secretsmanager_secret.auth.arn
}
