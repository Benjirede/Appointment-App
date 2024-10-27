# Placeholder for in-memory appointments
appointments_list = []

def get_appointments():
    return appointments_list

def add_appointment(name, time):
    appointments_list.append({'name': name, 'time': time})