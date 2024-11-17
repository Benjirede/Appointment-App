import csv
import os
import uuid
from datetime import datetime

CSV_FILE = 'appointments.csv'

# Initialize CSV and ensure headers are present
def initialize_csv():
    if not os.path.isfile(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'date', 'time'])

def read_appointments():
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        appointments = list(reader)
    return appointments

def write_appointment(name, date, time):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        appointment_id = str(uuid.uuid4())
        writer.writerow([appointment_id, name, date, time])

def is_time_valid(time):
    """Ensure the time is at a 15-minute interval."""
    time_object = datetime.strptime(time, "%H:%M")
    valid_minutes = {0, 15, 30, 45}
    return time_object.minute in valid_minutes

def is_slot_available(date, time):
    """Verify if the date and time slot is free."""
    appointments = read_appointments()
    return not any(
        appointment['date'] == date and appointment['time'] == time
        for appointment in appointments
    )

initialize_csv()