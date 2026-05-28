import boto3
import json
from backendLoanAssessment.schemas import MLLoanApplication

class SageMakerService:
    def __init__(self):
        self.client = boto3.client("sagemaker-runtime", region_name="us-east-1")
        self.endpoint_name = "loan-xgboost-endpoint-052820261350"

    def predict(self, ml_application: MLLoanApplication) -> dict:
        payload = ml_application.model_dump(by_alias=True)
        
        # convert to CSV row as it's what our XGBoost model expects
        csvRow = ",".join(str(v) for v in payload.values())

        response = self.client.invoke_endpoint(
            EndpointName=self.endpoint_name,
            ContentType="text/csv",
            Body=csvRow
        )
        
        result = json.loads(response["Body"].read().decode("utf-8"))
        return result