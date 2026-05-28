aws_region       = "us-east-1"
project_name     = "loan-preassessment-dev"
environment      = "dev"
training_data_s3 = "minh-loan-preassessment"

inference_image_uri   = "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:1.2-1-cpu-py3"
model_artifact_s3_uri = "s3://minh-loan-preassessment/output/loan-xgboost-job-005/output/model.tar.gz" # leave empty until after first training run
codecommit_repo_name  = "loan_preassessment_app"

