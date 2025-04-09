from datetime import datetime, timezone

from health_connector_base.handlers import Response
from health_connector_base.models import Appointment,Patient


def dashboard_handler(event, context):
    group_name = event["requestContext"]["authorizer"]["claims"]["cognito:groups"]
    ride_deletables = ["pickup", "dropoff"]
    res = []
    valid_patients = {
        patient.patient_id for patient in Patient.scan() if patient.via_rider_id and patient.via_rider_id.strip()
    }
    for mapping in Appointment.scan(Appointment.end_time >= datetime.now(timezone.utc)):
        if mapping.patient_id in valid_patients: 
            if group_name in [
                "DallasCountyHealthDepartmentHealthNavigators",
                "HealthcareFacilityStaff",
            ]:
                for deletable in ride_deletables:
                    mapping.ride[deletable] = {}
            res.append(mapping)

    return Response(res)
