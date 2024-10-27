from flask import Flask, render_template, request
from appointments import get_appointments, add_appointment

app = Flask(__name__)

@app.route('/')
def index():
    appointments = get_appointments()
    return render_template('index.html', appointments=appointments)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    time = request.form.get('time')
    if name and time:
        add_appointment(name, time)
    return index()

if __name__ == '__main__':
    app.run(debug=True)