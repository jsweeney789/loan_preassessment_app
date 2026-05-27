import time

while True:
    response = sm.describe_endpoint(
        EndpointName=endpoint_name
    )

    status = response["EndpointStatus"]

    print("Endpoint status:", status)

    if status == "InService":
        print("Endpoint is live!")
        break

    if status == "Failed":
        raise Exception(response["FailureReason"])

    time.sleep(30)