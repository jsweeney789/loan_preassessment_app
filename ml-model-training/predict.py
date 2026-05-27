import boto3
from dotenv import load_dotenv

load_dotenv()

runtime = boto3.client(
    "sagemaker-runtime",
    region_name="us-east-1"
)

endpoint_name = "loan-xgboost-endpoint"

payload = "67,2,2,0,1,1169,6"

response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="text/csv",
    Body=payload
)

result = response["Body"].read().decode()

print("Prediction:", result)