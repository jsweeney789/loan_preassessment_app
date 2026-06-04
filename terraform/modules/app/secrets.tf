# ── Google OAuth ──────────────────────────────────────────────────────────────
# Set value after apply:
# aws secretsmanager put-secret-value --secret-id dev/google-oauth \
#   --secret-string '{"client_secret":"YOUR_SECRET"}' --region us-east-1

resource "aws_secretsmanager_secret" "google_oauth" {
  name                    = "${var.environment}/google-oauth"
  recovery_window_in_days = var.environment == "prod" ? 7 : 0

  tags = merge(var.tags, {
    Name        = "${var.environment}-google-oauth"
    Environment = var.environment
  })
}

# ── Auth (JWT + Session) ──────────────────────────────────────────────────────
# Set value after apply:
# aws secretsmanager put-secret-value --secret-id dev/auth \
#   --secret-string '{"jwt_secret":"YOUR_JWT","session_secret":"YOUR_SESSION"}' --region us-east-1

resource "aws_secretsmanager_secret" "auth" {
  name                    = "${var.environment}/auth"
  recovery_window_in_days = var.environment == "prod" ? 7 : 0

  tags = merge(var.tags, {
    Name        = "${var.environment}-auth"
    Environment = var.environment
  })
}
