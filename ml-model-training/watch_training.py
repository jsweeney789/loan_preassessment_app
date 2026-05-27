import time
import boto3
from dotenv import load_dotenv

load_dotenv()

sm = boto3.client("sagemaker", region_name="us-east-1")

job_name = "loan-xgboost-job-005"

while True:
    response = sm.describe_training_job(TrainingJobName=job_name)
    status = response["TrainingJobStatus"]

    print("Status:", status)

    if status in ["Completed", "Failed", "Stopped"]:
        break

    time.sleep(10)