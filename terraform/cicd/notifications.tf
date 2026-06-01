# ── SNS Topic ─────────────────────────────────────────────────────────────────

resource "aws_sns_topic" "pipeline_notifications" {
  name = "${var.environment}-pipeline-notifications"

  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_sns_topic_subscription" "pipeline_email" {
  topic_arn = aws_sns_topic.pipeline_notifications.arn
  protocol  = "email"
  endpoint  = var.notification_email
}

# Allow EventBridge to publish to the topic
resource "aws_sns_topic_policy" "pipeline_notifications" {
  arn = aws_sns_topic.pipeline_notifications.arn

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "events.amazonaws.com" }
      Action    = "sns:Publish"
      Resource  = aws_sns_topic.pipeline_notifications.arn
    }]
  })
}

# ── EventBridge Rule ──────────────────────────────────────────────────────────

resource "aws_cloudwatch_event_rule" "pipeline_failure" {
  name        = "${var.environment}-pipeline-failure"
  description = "Triggers when any CI/CD pipeline execution fails"

  event_pattern = jsonencode({
    source      = ["aws.codepipeline"]
    "detail-type" = ["CodePipeline Pipeline Execution State Change"]
    detail = {
      state    = ["FAILED"]
      pipeline = [
        aws_codepipeline.backend.name,
        aws_codepipeline.frontend.name,
        aws_codepipeline.terraform.name,
      ]
    }
  })

  tags = merge(var.tags, { Environment = var.environment })
}

resource "aws_cloudwatch_event_target" "pipeline_failure_sns" {
  rule      = aws_cloudwatch_event_rule.pipeline_failure.name
  target_id = "PipelineFailureSNS"
  arn       = aws_sns_topic.pipeline_notifications.arn

  input_transformer {
    input_paths = {
      pipeline  = "$.detail.pipeline"
      state     = "$.detail.state"
      execution = "$.detail.execution-id"
      time      = "$.time"
    }
    input_template = "\"[<state>] Pipeline '<pipeline>' failed at <time>. Execution ID: <execution>. Check: https://console.aws.amazon.com/codesuite/codepipeline/pipelines/<pipeline>/view\""
  }
}
