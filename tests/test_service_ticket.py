from app import create_app
from app.models import db, Mechanic, ServiceTicket, Inventory, Customer
from datetime import datetime
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Adding a mechanic, customer, part, and service ticket for use during GET, PUT, and DELETE tests.
            customer = Customer(
                name="Jane Doe",
                email="jane@email.com",
                phone="1112223333",
                password="1234"
            )
            db.session.add(customer)
            db.session.commit()

            mechanic = Mechanic(
                name="John Mechanic",
                email="john@bodyshop.com",
                phone="337774444",
                salary=90000
            )
            db.session.add(mechanic)
            db.session.commit()

            part = Inventory(
                name="Front Bumper",
                price=139.50
            )
            db.session.add(part)
            db.session.commit()

            part = Inventory(
                name="Windshield",
                price=249.50
            )
            db.session.add(part)
            db.session.commit()

            service_ticket = ServiceTicket(
                vin="VIN123456H123456",
                service_date=datetime.strptime("2025-03-04", "%Y-%m-%d").date(),
                service_desc="Replace front bumper",
                customer_id=1
            )
            db.session.add(service_ticket)
            db.session.commit()

        self.client = self.app.test_client()

    def test_create_service_ticket(self):
        service_ticket_payload = {
        "vin": "NEWVIN1234567890",
        "service_date": "2024-02-28",
        "service_desc": "Replace windshield",
        "customer_id": 1
        }

        response = self.client.post('/service-tickets/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['vin'], "NEWVIN1234567890")
        self.assertEqual(response.json['service_desc'], "Replace windshield")
    
    def test_get_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['vin'], "VIN123456H123456")


    def test_login_cutomer(self): # need this to access the service tickets by customer route.
        credentials = {
            "email": "jane@email.com",
            "password": "1234"
        }
        response = self.client.post('/customers/login', json=credentials)
        return response.json['token']

    def test_service_tickets_by_customer(self):
        headers = {'Authorization': "Bearer " + self.test_login_cutomer()}
        response = self.client.get('/service-tickets/my-tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['service_desc'], "Replace front bumper")

    def test_add_mechanic_to_ticket(self): 
        update_payload = {
            "add_mechanic_ids": [1],
            "remove_mechanic_ids": []
        }

        response = self.client.put('/service-tickets/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['mechanics'][0]['name'], "John Mechanic") 
        self.assertEqual(response.json['service_date'], '2025-03-04')
    
    def test_add_mechanic_to_ticket(self):
        update_payload = {
            "add_part_id": 1,
        }

        response = self.client.put('/service-tickets/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['parts'][0]['name'], "Front Bumper") 
        self.assertEqual(response.json['service_date'], '2025-03-04')

    def test_delete_service_ticket(self):
        response = self.client.delete('/service-tickets/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Service ticket was successfully deleted', response.json.get('message', ''))

# python -m unittest discover tests