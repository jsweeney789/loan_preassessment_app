import boto3
from dotenv import load_dotenv

load_dotenv()

# check who you're authenticated as
sts = boto3.client("sts")
identity = sts.get_caller_identity()
print(identity)

s3 = boto3.client("s3")

response = s3.list_buckets()
for b in response["Buckets"]:
    print(b["Name"])

bucket = "minh-loan-preassessment"

response = s3.list_objects_v2(Bucket=bucket)

for obj in response.get("Contents", []):
    print(obj["Key"])

sm = boto3.client("sagemaker")

response = sm.list_training_jobs()
print(response)

print(sm.list_notebook_instances())
print(sm.list_endpoints())