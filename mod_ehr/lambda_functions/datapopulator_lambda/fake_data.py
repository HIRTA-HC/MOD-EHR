import csv
from datetime import datetime, timedelta

from faker import Faker

fake = Faker()


def generate_record():
    return {
        "Patient First Name": fake.first_name(),
        "Patient Middle Initial": fake.random_letter().upper(),
        "Patient Last Name": fake.last_name(),
        "Scheduling Location Description": fake.company(),
        "Appointment DateTime": (
            datetime.now() + timedelta(days=fake.random_int(min=1, max=30))
        ).strftime("%Y%m%d_%H%M%S"),
        "Status": fake.random_element(elements=("Booked", "Cancelled", "Pending")),
        "Patient Number": fake.uuid4(),
        "Appointment Duration": fake.random_int(min=15, max=120, step=30),
        "Location Name": "610",
        "Location Phone Number": fake.phone_number(),
        "Location Street1": "10th St",
        "Location Street2": "",
        "Location City": "Perry",
        "Location State": "IA",
        "Location Zip": "50220",
        "Appointment ID": fake.uuid4(),
    }


records = [generate_record() for _ in range(100)]

fieldnames = [
    "Patient First Name",
    "Patient Middle Initial",
    "Patient Last Name",
    "Scheduling Location Description",
    "Appointment DateTime",
    "Status",
    "Patient Number",
    "Appointment Duration",
    "Location Name",
    "Location Street1",
    "Location Street2",
    "Location City",
    "Location State",
    "Location Zip",
    "Location Phone Number",
    "Appointment ID",
]
with open("appointments.csv", "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="|")
    writer.writeheader()
    for record in records:
        writer.writerow(record)


print("CSV file with 100 records created successfully.")
