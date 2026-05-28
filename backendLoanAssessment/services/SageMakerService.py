import boto3
import json
import os
from backendLoanAssessment.schemas import MLLoanApplication
class SageMakerService:
    FEATURE_GROUPS = {
            "Age": [0],
            "Job": [1],
            "Housing": [2],
            "Saving accounts": [3],
            "Checking account": [4],
            "Credit amount": [5],
            "Duration": [6],
            "Sex": [7],
            "Purpose": [8, 9, 10, 11, 12, 13, 14],
        }
    def __init__(self, endpoint_name="loan-xgboost-endpoint"):
        self.client = boto3.client(
            "sagemaker-runtime",
            region_name="us-east-1",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )
        self.endpoint_name = endpoint_name

    def predictWithExplanations(self, mlApp: MLLoanApplication):
        # parse numerical LoanApplication into csv format
        payload = ",".join(str(v) for v in mlApp.model_dump(by_alias=True).values())

        # Make request
        response = self.client.invoke_endpoint(
            EndpointName=self.endpoint_name,
            ContentType="text/csv",
            Accept="text/csv",
            Body=payload
        )
        
        # Parse response
        raw_response = response["Body"].read().decode()
        result_json = json.loads(raw_response)
        
        # Get risk score
        probability = float(result_json["predictions"]["data"].strip())
        
        # Extract SHAP values
        raw_shap_values = result_json["explanations"]["kernel_shap"][0]
        
        # Parse raw SHAP values
        shap_dict = {}
        for idx, shap in enumerate(raw_shap_values):
            if isinstance(shap, dict) and "attributions" in shap:
                value = shap["attributions"][0]["attribution"][0]
            elif isinstance(shap, list):
                value = shap[0] if shap else 0
            else:
                value = shap
            shap_dict[idx] = value
        
        # Calculate grouped SHAP values
        grouped_shap = {}
        for group_name, indices in self.FEATURE_GROUPS.items():
            total_value = sum([shap_dict.get(idx, 0) for idx in indices])
            grouped_shap[group_name] = total_value
        
        return probability, grouped_shap