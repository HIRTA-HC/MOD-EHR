import os
import sys

if os.environ.get("ENVIRONMENT", "LOCAL") == "LOCAL":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from health_connector_base.constants import STRINGS, Status
from health_connector_base.handlers import Response
from health_connector_base.smart_epic import JWTHelper, SmartEpicClient


class EpicAppointmentsHandler:

    def _map_participants_data(
        self, appointment: dict, smart_client: SmartEpicClient
    ) -> dict:
        """
        Maps participant data from an appointment to a dictionary.

        Args:
            appointment (dict): The appointment data.
            smart_client (SmartEpicClient): The SmartEpicClient instance.
            start_time (int): The start time of the appointment.

        Returns:
            dict: A dictionary containing mapped participant data.
        """
        result = {}
        for participant in appointment["participant"]:
            participant_type = participant["actor"]["reference"]["@value"].split("/")
            if participant_type[0] == "Patient":
                result["patient_name"] = participant["actor"]["display"]["@value"]
                result["patient_id"] = participant_type[-1]
            elif participant_type[0] == "Location":
                if location_response := smart_client.get_location_data(
                    participant_type[-1]
                ):
                    result["location"] = location_response
        return result

    def __call__(self, event):

        if not (patient_id := (event.get("pathParameters") or {}).get("id")):
            return Response(status=Status.HTTP_422_UNPROCESSABLE_ENTITY)
        smart_client = SmartEpicClient(JWTHelper().generate_jwt())
        if not (appointments := smart_client.get_appointments(patient_id)):
            return Response(
                {
                    "message": STRINGS["EPIC_APPOINTMENTS_NOT_FOUND"]
                    % {"patient_id": patient_id}
                }
            )
        if (event.get("queryStringParameters") or {}).get("minified") == "True":
            data = []
            for appointment in appointments["Bundle"]["entry"]:
                try:
                    appointment = appointment["resource"]["Appointment"]
                    status = appointment["status"]["@value"]
                    if status != "arrived":
                        start_time = appointment["start"]["@value"]
                        end_time = appointment["start"]["@value"]
                        result = {
                            "id": appointment["id"]["@value"],
                            "status": status,
                            "start_time": start_time,
                            "end_time": end_time,
                            "provider": "epic",
                        } | self._map_participants_data(appointment, smart_client)
                        data.append(result)
                except KeyError as e:
                    print(e.args)
            return Response(data)
        return Response(appointments)


def epic_handler(event, context):
    return EpicAppointmentsHandler()(event)
