resource "random_password" "db" {
  length           = 32
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

# ── Secrets Manager ───────────────────────────────────────────────────────────

resource "aws_secretsmanager_secret" "db" {
  name                    = "${var.environment}/db"
  recovery_window_in_days = var.environment == "prod" ? 7 : 0

  tags = merge(var.tags, {
    Name        = "${var.environment}-db-credentials"
    Environment = var.environment
  })
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id = aws_secretsmanager_secret.db.id
  secret_string = jsonencode({
    username = var.db_username
    password = random_password.db.result
    host     = aws_db_instance.db.address
    port     = aws_db_instance.db.port
    dbname   = var.db_name
  })
}

# ── Subnet group ──────────────────────────────────────────────────────────────

resource "aws_db_subnet_group" "db" {
  name       = "${var.environment}-db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = merge(var.tags, {
    Name        = "${var.environment}-db-subnet-group"
    Environment = var.environment
  })
}

# ── Parameter group ───────────────────────────────────────────────────────────

resource "aws_db_parameter_group" "db" {
  name   = "${var.environment}-db-parameter-group"
  family = "postgres16"

  parameter {
    name  = "log_connections"
    value = "1"
  }

  parameter {
    name  = "log_min_duration_statement"
    value = "1000"
  }

  tags = merge(var.tags, {
    Name        = "${var.environment}-db-parameter-group"
    Environment = var.environment
  })
}

# ── RDS instance ──────────────────────────────────────────────────────────────

resource "aws_db_instance" "db" {
  identifier = "${var.environment}-loan-db"

  engine         = "postgres"
  engine_version = var.db_engine_version
  instance_class = var.db_instance_class

  db_name  = var.db_name
  username = var.db_username
  password = random_password.db.result

  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = var.db_max_allocated_storage
  storage_type          = "gp3"
  storage_encrypted     = true

  db_subnet_group_name   = aws_db_subnet_group.db.name
  vpc_security_group_ids = [var.rds_sg_id]
  parameter_group_name   = aws_db_parameter_group.db.name

  multi_az               = var.multi_az
  backup_retention_period = var.backup_retention_days
  skip_final_snapshot    = var.environment == "prod" ? false : true
  final_snapshot_identifier = var.environment == "prod" ? "${var.environment}-loan-db-final" : null
  deletion_protection    = var.environment == "prod" ? true : false

  performance_insights_enabled = true

  tags = merge(var.tags, {
    Name        = "${var.environment}-loan-db"
    Environment = var.environment
  })
}
