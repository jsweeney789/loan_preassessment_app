output "db_endpoint" {
  description = "RDS instance endpoint (host:port)"
  value       = aws_db_instance.db.endpoint
}

output "db_host" {
  description = "RDS instance hostname"
  value       = aws_db_instance.db.address
}

output "db_port" {
  description = "RDS instance port"
  value       = aws_db_instance.db.port
}

output "db_name" {
  description = "Database name"
  value       = aws_db_instance.db.db_name
}

output "db_secret_arn" {
  description = "Secrets Manager ARN containing the DB credentials (username, password, host, port, dbname)"
  value       = aws_secretsmanager_secret.db.arn
}

output "db_instance_id" {
  description = "RDS instance identifier"
  value       = aws_db_instance.db.identifier
}
