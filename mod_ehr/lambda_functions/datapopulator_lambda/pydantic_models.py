from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class Appointment(BaseModel):
    patient_first_name: str = Field(..., alias="Patient First Name")
    patient_middle_initial: Optional[str] = Field(None, alias="Patient Middle Initial")
    patient_last_name: str = Field(..., alias="Patient Last Name")
    scheduling_location_description: str = Field(
        ..., alias="Scheduling Location Description"
    )
    appointment_datetime: datetime = Field(..., alias="Appointment DateTime")
    status: str = Field(..., alias="Status")
    location_phone_number: str = Field(..., alias="Location Phone Number")
    patient_number: str = Field(..., alias="Patient Number")
    appointment_duration: int = Field(..., alias="Appointment Duration")
    location_street1: str = Field(..., alias="Location Street1")
    location_street2: Optional[str] = Field(None, alias="Location Street2")
    location_city: str = Field(..., alias="Location City")
    location_state: str = Field(..., alias="Location State")
    location_zip: str = Field(..., alias="Location Zip")
    location_name: str = Field(..., alias="Location Name")
    appointment_id: str = Field(..., alias="Appointment ID")

    class Config:
        populate_by_name = True

    check_fields: bool | None = (...,)

    @field_validator("appointment_datetime", mode="before")
    def validate_appointment_datetime(cls, v):
        try:
            # Attempt to parse the datetime string
            return datetime.strptime(v, "%Y%m%d_%H%M%S")
        except ValueError as e:
            raise ValueError(
                "Invalid datetime format. Should be YYYYMMDD_HHMMSS"
            ) from e

    @field_validator("*", mode="after")
    def replace_none_with_empty_string(cls, v):
        return "" if v is None else (v.strip() if isinstance(v, str) else v)


class AppointmentsList(BaseModel):
    appointments: list[Appointment]

    class Config:
        arbitrary_types_allowed = True
