# ── ALB Security Group (public-facing) ───────────────────────────────────────

resource "aws_security_group" "alb" {
  name        = "${var.environment}-alb-sg"
  description = "Allow inbound HTTP/HTTPS from the internet"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name        = "${var.environment}-alb-sg"
    Environment = var.environment
  })
}

# ── ECS Security Group (only accepts traffic from ALB) ───────────────────────

resource "aws_security_group" "ecs" {
  name        = "${var.environment}-ecs-sg"
  description = "Allow inbound traffic from ALB only"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "From ALB"
    from_port       = var.app_port
    to_port         = var.app_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, {
    Name        = "${var.environment}-ecs-sg"
    Environment = var.environment
  })
}

# ── RDS Security Group (only accepts traffic from ECS) ───────────────────────

# resource "aws_security_group" "rds" {
#   name        = "${var.environment}-rds-sg"
#   description = "Allow inbound PostgreSQL from ECS only"
#   vpc_id      = aws_vpc.main.id

#   ingress {
#     description     = "PostgreSQL from ECS"
#     from_port       = 5432
#     to_port         = 5432
#     protocol        = "tcp"
#     security_groups = [aws_security_group.ecs.id]
#   }

#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   tags = merge(var.tags, {
#     Name        = "${var.environment}-rds-sg"
#     Environment = var.environment
#   })
# }

# ── SageMaker Security Group (only accepts traffic from ECS) ─────────────────

# resource "aws_security_group" "sagemaker" {
#   name        = "${var.environment}-sagemaker-sg"
#   description = "Allow inbound HTTPS from ECS for model inference"
#   vpc_id      = aws_vpc.main.id

#   ingress {
#     description     = "HTTPS from ECS"
#     from_port       = 443
#     to_port         = 443
#     protocol        = "tcp"
#     security_groups = [aws_security_group.ecs.id]
#   }

#   egress {
#     from_port   = 0
#     to_port     = 0
#     protocol    = "-1"
#     cidr_blocks = ["0.0.0.0/0"]
#   }

#   tags = merge(var.tags, {
#     Name        = "${var.environment}-sagemaker-sg"
#     Environment = var.environment
#   })
# }
