import boto3
from dotenv import load_dotenv

load_dotenv()

runtime = boto3.client(
    "sagemaker-runtime",
    region_name="us-east-1"
)

endpoint_name = "loan-xgboost-endpoint-052820261048"

payload = "40,3,2,0,1,1977,36,1,0,0,1,0,0,0,0"

response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType="text/csv",
    Body=payload
)

result = response["Body"].read().decode()

print("Prediction:", result)