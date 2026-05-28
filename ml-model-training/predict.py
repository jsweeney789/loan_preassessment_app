import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_shap_explanations(payload, endpoint_name="loan-xgboost-endpoint"):

    runtime = boto3.client(
        "sagemaker-runtime",
        region_name="us-east-1",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
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
    
    # Make request
    response = runtime.invoke_endpoint(
        EndpointName=endpoint_name,
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
    for group_name, indices in FEATURE_GROUPS.items():
        total_value = sum([shap_dict.get(idx, 0) for idx in indices])
        grouped_shap[group_name] = total_value
    
    return probability, grouped_shap


# Example usage and parsing

'''
if __name__ == "__main__":

    payload = "20,1,1,1,2,2718,24,0,1,0,0,0,0,0,0"
    
    # Get explanations
    probability, shap_values = get_shap_explanations(payload)
    
    # Print results
    # I think I like low score = bad, high score = good
    print(f"\nLoan score          : {100-probability*100:.0f}\n")

    for feature, value in shap_values.items():
        # Only SHAPs more extreme than 0.15
        if (abs(value) >= 0.15):
            print(f"{feature:<20}: {-value:+.4f}")
'''