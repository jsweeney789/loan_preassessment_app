# ── SageMaker Model + Endpoint ────────────────────────────────────────────────

# locals {
#   deploy_endpoint = var.model_artifact_s3_uri != ""
# }

resource "aws_sagemaker_model" "loan" {

  name               = "${var.environment}-loan-assessment"
  execution_role_arn = aws_iam_role.sagemaker_execution.arn

  primary_container {
    image          = var.inference_image_uri
    model_data_url = var.model_artifact_s3_uri
    # No SAGEMAKER_PROGRAM — the sklearn container's built-in handlers are used:
    #   model_fn   → loads model.joblib from the extracted artifact directory
    #   predict_fn → calls model.predict()
    # Add environment vars here only if a custom inference.py is ever needed
  }

  tags = merge(var.tags, {
    Name        = "${var.environment}-loan-assessment-model"
    Environment = var.environment
  })
}

# resource "aws_sagemaker_endpoint_configuration" "loan" {
#   count = local.deploy_endpoint ? 1 : 0

#   name = "${var.environment}-loan-assessment"

#   production_variants {
#     variant_name = "primary"
#     model_name   = aws_sagemaker_model.loan[0].name

#     serverless_config {
#       max_concurrency   = 2
#       memory_size_in_mb = 3072  # sklearn + xgboost need headroom; 1024 causes cold-start timeouts
#     }
#   }

#   tags = merge(var.tags, {
#     Name        = "${var.environment}-loan-assessment-endpoint-config"
#     Environment = var.environment
#   })
# }

# resource "aws_sagemaker_endpoint" "loan" {
#   count = local.deploy_endpoint ? 1 : 0

#   name                 = "${var.environment}-loan-assessment"
#   endpoint_config_name = aws_sagemaker_endpoint_configuration.loan[0].name

#   lifecycle {
#     ignore_changes = [endpoint_config_name]
#   }

#   tags = merge(var.tags, {
#     Name        = "${var.environment}-loan-assessment-endpoint"
#     Environment = var.environment
#   })
# }