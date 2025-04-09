import os
import json
import boto3
from health_connector_base import models
from health_connector_base.handlers import APIHandler

environment = os.environ.get("ENVIRONMENT", "LOCAL")


class AppointmentAPIHandler(APIHandler):
    model = models.Appointment

    @classmethod
    def process_event(cls, event: dict, *args, **kwargs):
        response = super(AppointmentAPIHandler, cls).process_event(
            event, *args, **kwargs
        )
        
        if event["httpMethod"].lower() != "get":
            lambda_client = boto3.client("lambda")
            lambda_client.invoke(
                FunctionName=f"HealthConnector{environment.title()}DataPopulator",
                InvocationType="Event",
                Payload=b"{}",
            )
        if isinstance(response, dict) and "body" in response:
            try:
                # Parse the body JSON
                response_body = json.loads(response["body"])

                # Filter required fields
                if isinstance(response_body, list):  # Ensure it's a list of appointments
                    filtered_data = [
                        {
                            "id": item["id"],
                            "location": item["location"],
                            "patient_name": item["patient_name"],
                            "start_time": item["start_time"],
                            "end_time": item["end_time"],
                            "status": item["status"]
                        }
                        for item in response_body
                        if all(k in item for k in ["id", "location", "patient_name", "start_time", "end_time", "status"])
                    ]

                    # Update response body
                    response["body"] = json.dumps(filtered_data)

            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
        return response


def appointments_handler(event, context):
    return AppointmentAPIHandler.process_event(event)
