from app import create_app
from app.models import db, Mechanic, Customer, ServiceTicket, Inventory
from datetime import datetime
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Adding a mechanic, customer, part, and service ticket for use during GET, PUT, and DELETE tests.
            mechanic = Mechanic(
                name="John Mechanic",
                email="john@bodyshop.com",
                phone="337774444",
                salary=90000
            )
            db.session.add(mechanic)
            db.session.commit()

            customer = Customer(
                name="Jane Doe",
                email="jane@email.com",
                phone="1112223333",
                password="1234"
            )
            db.session.add(customer)
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
        print(response.json)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['vin'], "NEWVIN1234567890")
        self.assertEqual(response.json['service_desc'], "Replace windshield")
    
    def test_get_service_tickets(self):
        response = self.client.get('/service-tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['vin'], "VIN123456H123456")

    # def test_update_mechanic(self): # TODO change the route in blueprints to accept empty parts
    #     update_payload = {
    #         "name": "Bobby Mechanic",
    #         "email": "bobby@bodyshop.com",
    #         "phone": "337774444",
    #         "salary": 80000
    #     }

    #     response = self.client.put('/mechanics/1', json=update_payload)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json['name'], 'Bobby Mechanic') 
    #     self.assertEqual(response.json['email'], 'bobby@bodyshop.com')
    
    # def test_delete_mechanic(self):
    #     response = self.client.delete('/mechanics/1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Mechanic removed successfully', response.json.get('message', ''))
    
    # def test_delete_nonexistent_mechanic(self):
    #     response = self.client.delete('/mechanics/10')
    #     self.assertEqual(response.status_code, 404)

# python -m unittest discover tests