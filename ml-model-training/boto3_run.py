import time
import boto3
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

sm = boto3.client("sagemaker", region_name="us-east-1")

role_arn = "arn:aws:iam::397345411365:role/dev-sagemaker-execution-role"

# Unique timestamp in MMDDYYYYHHMM format
timestamp = datetime.now().strftime("%m%d%Y%H%M")
training_job_name = f"loan-xgboost-job-{timestamp}"

# -------------------------
# START TRAINING
# -------------------------

sm.create_training_job(
    TrainingJobName=training_job_name,

    RoleArn=role_arn,

    AlgorithmSpecification={
        "TrainingImage": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.7-1",
        "TrainingInputMode": "File"
    },

    HyperParameters={
        "objective": "binary:logistic",
        "num_round": "50",
        "eta": "0.1",
        "scale_pos_weight": "11.515151515151515",
        # "enable_categorical": "true" 
    },

    InputDataConfig=[
        {
            "ChannelName": "train",
            "DataSource": {
                "S3DataSource": {
                    "S3DataType": "S3Prefix",
                    "S3Uri": "s3://minh-loan-preassessment/training-data/german_credit_data_onehot.csv",
                    "S3DataDistributionType": "FullyReplicated"
                }
            },
            "ContentType": "csv"
        }
    ],

    OutputDataConfig={
        "S3OutputPath": "s3://minh-loan-preassessment/output/"
    },

    ResourceConfig={
        "InstanceType": "ml.m5.large",
        "InstanceCount": 1,
        "VolumeSizeInGB": 10
    },

    StoppingCondition={
        "MaxRuntimeInSeconds": 3600
    }
)

print("Training started")

# -------------------------
# WAIT FOR TRAINING
# -------------------------

while True:
    response = sm.describe_training_job(
        TrainingJobName=training_job_name
    )

    status = response["TrainingJobStatus"]

    print("Training status:", status)

    if status == "Completed":
        break

    if status == "Failed":
        raise Exception(response["FailureReason"])

    time.sleep(30)

# -------------------------
# CREATE MODEL
# -------------------------

model_name = f"loan-xgboost-model-{timestamp}"

model_data_url = (
    f"s3://minh-loan-preassessment/output/"
    f"{training_job_name}/output/model.tar.gz"
)

sm.create_model(
    ModelName=model_name,
    ExecutionRoleArn=role_arn,
    PrimaryContainer={
        "Image": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-xgboost:1.7-1",
        "ModelDataUrl": model_data_url
    }
)

print("Model created")

# -------------------------
# CREATE ENDPOINT CONFIG
# -------------------------

endpoint_config_name = f"loan-xgboost-config-{timestamp}"

sm.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ProductionVariants=[
        {
            "VariantName": "AllTraffic",
            "ModelName": model_name,
            "ServerlessConfig": {      
                # these are the values that specify how our Serverless endpoint works and Claude gave me these knowing this was a
                # small app for learning, be aware that these are small. Also be aware that as this is serverless there is a cold start delay of a few seconds
                "MemorySizeInMB": 2048, 
                "MaxConcurrency": 5
            }
        }
    ]
)

print("Endpoint config created")

# -------------------------
# CREATE ENDPOINT
# -------------------------

endpoint_name = f"loan-xgboost-endpoint-{timestamp}"

sm.create_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=endpoint_config_name
)

print("Endpoint deployment started")

### Watch endpoint go live

import time


while True:
    response = sm.describe_endpoint(
        EndpointName=endpoint_name
    )

    status = response["EndpointStatus"]

    print("Endpoint status:", status)

    if status == "InService":
        print(f"Endpoint is live at:\n{endpoint_name}")
        break

    if status == "Failed":
        raise Exception(response["FailureReason"])

    time.sleep(30)