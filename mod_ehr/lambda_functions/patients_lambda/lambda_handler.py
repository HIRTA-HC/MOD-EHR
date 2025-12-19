import os
import sys

if os.environ.get("ENVIRONMENT", "LOCAL") == "LOCAL":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from health_connector_base import models
from health_connector_base.handlers import APIHandler, Response
from health_connector_base.models import Patient


class PatientsHandler(APIHandler):
    model = models.Patient

    def get(self, event, hash_key=None, *args, **kwargs):
        if hash_key:
            return self.retrieve(event, hash_key, *args, **kwargs)
        # Only return patients with a non-empty via_rider_id
        filtered_patients = [
            p for p in Patient.scan(
                filter_condition = Patient.via_rider_id.exists() & (Patient.via_rider_id != "")
            )
            # if getattr(p, "via_rider_id", None) and p.via_rider_id.strip() != ""
        ]
        return Response(body=filtered_patients, status=200)


def patients_handler(event, context):
    return PatientsHandler.process_event(event)
