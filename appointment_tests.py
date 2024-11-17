import unittest
from flask import Flask
from app import app
from appointments import read_appointments, initialize_csv
import os
import csv

class TestAppointmentSystem(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Create a temporary test CSV file
        self.test_csv = 'test_appointments.csv'
        app.config['CSV_FILE'] = self.test_csv
        
        # Initialize the test CSV file
        with open(self.test_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'date', 'time'])

    def tearDown(self):
        # Clean up the test CSV file after each test
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_add_valid_appointment(self):
        """Test adding a valid appointment"""
        response = self.client.post('/appointments/add', data={
            'name': 'John Doe',
            'date': '2024-12-01',
            'time': '09:15'
        }, follow_redirects=True)
        
        # Check if the request was successful
        self.assertEqual(response.status_code, 200)
        
        # Read the appointments and verify the new appointment was added
        appointments = read_appointments()
        self.assertEqual(len(appointments), 1)
        self.assertEqual(appointments[0]['name'], 'John Doe')
        self.assertEqual(appointments[0]['date'], '2024-12-01')
        self.assertEqual(appointments[0]['time'], '09:15')

    def test_add_invalid_time_appointment(self):
        """Test adding an appointment with invalid time (not 15-min interval)"""
        response = self.client.post('/appointments/add', data={
            'name': 'Jane Doe',
            'date': '2024-12-01',
            'time': '09:10'
        }, follow_redirects=True)
        
        # Verify that the appointment wasn't added
        appointments = read_appointments()
        self.assertEqual(len(appointments), 0)

    def test_add_duplicate_appointment(self):
        """Test adding an appointment to an already occupied time slot"""
        # First, add a valid appointment
        self.client.post('/appointments/add', data={
            'name': 'John Doe',
            'date': '2024-12-01',
            'time': '09:15'
        })
        
        # Try to add another appointment at the same time
        response = self.client.post('/appointments/add', data={
            'name': 'Jane Doe',
            'date': '2024-12-01',
            'time': '09:15'
        }, follow_redirects=True)
        
        # Verify that only one appointment exists
        appointments = read_appointments()
        self.assertEqual(len(appointments), 1)
        self.assertEqual(appointments[0]['name'], 'John Doe')

    def test_add_appointment_missing_data(self):
        """Test adding an appointment with missing required fields"""
        response = self.client.post('/appointments/add', data={
            'name': 'John Doe',
            # Missing date and time
        }, follow_redirects=True)
        
        # Verify no appointment was added
        appointments = read_appointments()
        self.assertEqual(len(appointments), 0)

if __name__ == '__main__':
    unittest.main()
