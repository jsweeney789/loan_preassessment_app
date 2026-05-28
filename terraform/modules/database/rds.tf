

resource "aws_db_subnet_group" "db" {
  name       = "${var.environment}-db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = merge(vars.tags,{
     Name = "${var.environment}-db-subnet-group"
     Environment = var.environment
  }
  )
}

resource "aws_db_parameter_group" "db" {
  name   = "${var.environment}-db-parameter-group"
  family = "postgres16"

  parameter {
    name  = "character_set_server"
    value = "utf8"
  }

  parameter {
    name  = "character_set_client"
    value = "utf8"
  }
}



resource "aws_db_instance" "db" {
  allocated_storage    = 3
  db_name              = var.db_name
  engine               = "postgres"
  engine_version       = var.db_engine_version
  instance_class       = var.db_instance_class
  username             = var.db_username
  password             = var.db_password
  parameter_group_name = "default.mysql8.0"
  skip_final_snapshot  = true
}