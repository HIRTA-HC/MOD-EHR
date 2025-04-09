import os
import sys

if os.environ.get("ENVIRONMENT", "LOCAL") == "LOCAL":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from health_connector_base import models
from health_connector_base.handlers import APIHandler


class PatientsHandler(APIHandler):
    model = models.Patient


def patients_handler(event, context):
    return PatientsHandler.process_event(event)
