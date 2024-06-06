import contextlib
from datetime import datetime, timezone
from functools import cached_property

from health_connector_base.constants import DIFF_MATCH_IN_SEC, MOCK_DATA, VIA_RIDE_MOCK
from health_connector_base.location_manager import LocationManager
from health_connector_base.models import Appointment, Dashboard, Patient, Settings
from health_connector_base.smart_epic import JWTHelper, SmartEpicClient
from health_connector_base.via import Via


class AppointmentsMapperWithVia:
    """
    Returns the patient-rider mapping as a dictionary.
    Returns:
        dict: The patient-rider mapping.
    """

    settings = ["subsequent_period", "prior_period"]

    @cached_property
    def prior_period(self):
        with contextlib.suppress(Settings.DoesNotExist):
            return int(Settings.get("prior_period")) * 60
        return DIFF_MATCH_IN_SEC

    @cached_property
    def subsequent_period(self):
        with contextlib.suppress(Settings.DoesNotExist):
            return int(Settings.get("subsequent_period")) * -60
        return 900

    def patient_mapping(self) -> dict:
        """
        Returns the patient-rider mapping as a dictionary.
        Returns:
            dict: The patient-rider mapping.
        """
        return {
            "epic": {
                patient.epic_id: patient.via_rider_id for patient in Patient.scan()
            }
        }

    def _get_jwt(self):
        """
        Generates a JWT token.
        Returns:
            The generated JWT token.
        """

        return JWTHelper().generate_jwt()

    def _map_participant_details(self, participant: dict):
        """
        Maps the details of a participant.
        Args:
            participant_type (list): The type of participant.
            participant (dict): The participant details.
        Returns:
            dict: The mapped participant details.
        """
        return participant["actor"]["display"]["@value"]

    def get_matching_ride(
        self, address: str, trips: list, appointment_start_time: int
    ) -> dict:
        """
        Returns the matching ride based on the address, trips, and appointment start time.
        Args:
            address (str): The address.
            trips (list): The list of trips.
            appointment_start_time (int): The appointment start timestamp..
        Returns:
            The matching ride.
        """
        match_ride = {}
        prev_diff = 1e9
        location_diff = 1e9
        for trip in trips:
            cur_diff = appointment_start_time - trip["dropoff_eta"]
            cur_location_diff = LocationManager().get_distance_from_address_coords(
                address,
                [
                    trip.get("dropoff", {}).get("lat", 0),
                    trip.get("dropoff", {}).get("lng", 0),
                ],
            )
            if (
                self.subsequent_period <= cur_diff <= self.prior_period
                and cur_diff < prev_diff
                and cur_location_diff <= location_diff
            ):
                prev_diff = cur_diff
                match_ride = trip
                location_diff = cur_location_diff
        return match_ride

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

    def epic_with_via(self, patient_mapping: dict):
        smart_client = SmartEpicClient(self._get_jwt())
        data = []
        for patient_key, rider_id in patient_mapping["epic"].items():
            if appointments := smart_client.get_appointments(patient_key):
                trips = Via().get_trips(rider_id).get("trips")
                for appointment in appointments["Bundle"]["entry"]:
                    try:
                        appointment = appointment["resource"]["Appointment"]
                        status = appointment["status"]["@value"]
                        if status != "arrived":
                            start_time = appointment["start"]["@value"]
                            end_time = appointment["end"]["@value"]
                            start_time = int(
                                datetime.strptime(
                                    start_time, "%Y-%m-%dT%H:%M:%SZ"
                                ).timestamp()
                            )
                            end_time = int(
                                datetime.strptime(
                                    end_time, "%Y-%m-%dT%H:%M:%SZ"
                                ).timestamp()
                            )
                            result = {
                                "id": appointment["id"]["@value"],
                                "status": status,
                                "start_time": start_time,
                                "end_time": end_time,
                                "provider": "epic",
                            } | self._map_participants_data(appointment, smart_client)
                            result["ride"] = (
                                self.get_matching_ride(
                                    result["location"],
                                    trips,
                                    appointment_start_time=start_time,
                                )
                                or VIA_RIDE_MOCK
                            )
                            data.append(result)
                    except KeyError as e:
                        print(e.args)
        return data

    def veradigm_with_via(self, patient_mapping):
        """
        # TODO
        """

    def __call__(self, *args, **kwargs):

        patient_mapping = self.patient_mapping()
        data = self.epic_with_via(patient_mapping)
        print(data)
        for item in Dashboard.scan():
            item.delete()
        with Dashboard.batch_write() as batch:
            for mapping in data:
                batch.save(Dashboard(**mapping))


class AppointmentsMapperWithViaMock(AppointmentsMapperWithVia):

    def epic_with_via(self, patient_mapping):
        data = []
        deletable = []
        patient_trips = {}
        for appointment in Appointment.scan():
            if (appointment.end_time >= datetime.now(timezone.utc)) and (
                appointment.status == "Booked"
            ):
                if rider_id := patient_mapping["epic"].get(appointment.patient_id):
                    start_time = int(appointment.start_time.timestamp())
                    end_time = int(appointment.end_time.timestamp())
                    trips = patient_trips.get(appointment.patient_id)
                    if trips is None:
                        trips = Via().get_trips(rider_id)
                        patient_trips[appointment.patient_id] = trips
                    data.append(
                        {
                            "id": appointment.id,
                            "patient_id": appointment.patient_id,
                            "patient_name": appointment.patient_name,
                            "status": appointment.status,
                            "location": appointment.location,
                            "start_time": start_time,
                            "end_time": end_time,
                            "provider": "epic",
                            "ride": self.get_matching_ride(
                                appointment.location, trips.get("trips"), start_time
                            )
                            or VIA_RIDE_MOCK,
                        }
                    )
            else:
                deletable.append(appointment.id)

        return data


def data_populator(*args, **kwargs):
    if MOCK_DATA:
        AppointmentsMapperWithViaMock()()
    else:
        AppointmentsMapperWithVia()()


if __name__ == "__main__":
    data_populator()
