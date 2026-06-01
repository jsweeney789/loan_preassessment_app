import time
import boto3
import json
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

# Hardcoded SHAP baseline values calculated from training data (feature means)
# print(",".join([str(x) for x in df.drop(columns=['Credit Risk']).mean().values]))
shap_baseline = "35.501048218029354,1.909853249475891,1.6027253668763102,1.1907756813417192,1.0576519916142557,3279.1121593291405,20.78092243186583,0.6876310272536688,0.33752620545073375,0.012578616352201259,0.06079664570230608,0.18343815513626835,0.2746331236897275,0.020964360587002098,0.012578616352201259"

sm.create_endpoint_config(
    EndpointConfigName=endpoint_config_name,
    ProductionVariants=[
        {
            "VariantName": "variant1",
            "ModelName": model_name,
            "InstanceType": "ml.m5.large",
            "InitialInstanceCount": 1,
        }
    ],
    ExplainerConfig={
        "ClarifyExplainerConfig": {
            "InferenceConfig": {
                "MaxPayloadInMB": 6,
                "MaxRecordCount": 200,
                "ProbabilityAttribute": "predictions.data"
            },
            "ShapConfig": {
                "ShapBaselineConfig": {
                    "ShapBaseline": shap_baseline
                },
                "NumberOfSamples": 100,
                "UseLogit": True,
                "Seed": 7777777
            }
        }
    }
)

print("Endpoint config created")

# -------------------------
# CREATE ENDPOINT
# -------------------------

endpoint_name = f"loan-xgboost-endpoint"

sm.create_endpoint(
    EndpointName=endpoint_name,
    EndpointConfigName=endpoint_config_name
)

print("Endpoint deployment started")

### Watch endpoint go live

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