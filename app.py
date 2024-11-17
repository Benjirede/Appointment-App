from flask import Flask, render_template, request, redirect, url_for, flash
from appointments import read_appointments, write_appointment, is_time_valid, is_slot_available
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling (flashing messages)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/appointments', methods=['GET'])
def view_appointments():
    appointments = read_appointments()
    return render_template('view_appointments.html', appointments=appointments)

@app.route('/appointments/add', methods=['GET'])
def add_appointment_form():
    return render_template('add_appointment.html')

@app.route('/appointments/add', methods=['POST'])
def add_appointment():
    name = request.form['name']
    date = request.form['date']
    time = request.form['time']

    # Validate 15-minute intervals and availability
    if not is_time_valid(time):
        flash("Invalid time. Appointments must be on the hour, 15, 30, or 45 past.")
        return redirect(url_for('add_appointment_form'))

    if not is_slot_available(date, time):
        flash("This time slot is already occupied. Please choose another time.")
        return redirect(url_for('add_appointment_form'))

    # If valid, write the appointment
    write_appointment(name, date, time)
    return redirect(url_for('view_appointments'))

@app.template_filter('format_time')
def format_time(value):
    try:
        time_object = datetime.strptime(value, "%H:%M")
        return time_object.strftime("%I:%M %p")
    except ValueError:
        return value

if __name__ == '__main__':
    app.run(debug=True)