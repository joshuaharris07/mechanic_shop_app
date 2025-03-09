from app import create_app
from app.models import db, Mechanic, ServiceTicket
from datetime import datetime
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Adding a mechanic for use during GET, PUT, and DELETE tests.
            mechanic = Mechanic(
                name="John Mechanic",
                email="john@bodyshop.com",
                phone="3337774444",
                salary=90000
            )
            db.session.add(mechanic)
            db.session.commit()

        self.client = self.app.test_client()
    
    def test_create_mechanic(self):
        mechanic_payload = {
        "name": "Jane Mechanic",
        "email": "jane@bodyshop.com",
        "phone": "3337774444",
        "salary": 70000
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Jane Mechanic")
        self.assertEqual(response.json['salary'], 70000)
    
    def test_get_mechanics(self):
        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], "John Mechanic")

    def test_update_mechanic(self): 
        update_payload = {
            "name": "Bobby Mechanic",
            "email": "bobby@bodyshop.com",
            "phone": "",
            "salary": 90000,
        }

        response = self.client.put('/mechanics/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Bobby Mechanic') 
        self.assertEqual(response.json['email'], 'bobby@bodyshop.com')
        self.assertEqual(response.json['phone'], '3337774444')
    
    def test_delete_mechanic(self):
        response = self.client.delete('/mechanics/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Mechanic removed successfully', response.json.get('message', ''))
    
    def test_delete_nonexistent_mechanic(self):
        response = self.client.delete('/mechanics/10')
        self.assertEqual(response.status_code, 404)

    
    def test_sort_mechanics_by_tickets(self):
        with self.app.app_context():
            # Create mechanics
            mechanic1 = Mechanic(
                name="Alice",
                email="alice@bodyshop.com",
                phone="1111111111",
                salary=95000
            )
            mechanic2 = Mechanic(
                name="Bob",
                email="bob@bodyshop.com",
                phone="2222222222",
                salary=87000
            )
            mechanic3 = Mechanic(
                name="Charlie",
                email="charlie@bodyshop.com",
                phone="3333333333",
                salary=80000
            )

            db.session.add_all([mechanic1, mechanic2, mechanic3])
            db.session.commit()

            # Assign service tickets to mechanics
            ticket1 = ServiceTicket(
                vin="VIN123456H123456",
                service_date=datetime.strptime("2025-03-04", "%Y-%m-%d").date(),
                service_desc="Fix brakes",
                customer_id=1,
                mechanics=[mechanic1]
            )
            ticket2 = ServiceTicket(
                vin="VIN789101J789101",
                service_date=datetime.strptime("2025-03-05", "%Y-%m-%d").date(),
                service_desc="Oil change",
                customer_id=1,
                mechanics=[mechanic1]
            )
            ticket3 = ServiceTicket(
                vin="VIN111213K111213",
                service_date=datetime.strptime("2025-03-06", "%Y-%m-%d").date(),
                service_desc="Engine check",
                customer_id=1,
                mechanics=[mechanic2]
            )

            db.session.add_all([ticket1, ticket2, ticket3])
            db.session.commit()

        response = self.client.get('/mechanics/most-tickets')
        self.assertEqual(response.status_code, 200)
        data = response.json

        # Make sure the first two are Alice and Bob
        self.assertEqual(data[0]['name'], 'Alice')
        self.assertEqual(data[0]['email'], 'alice@bodyshop.com')

        self.assertEqual(data[1]['name'], 'Bob')
        self.assertEqual(data[1]['salary'], 87000)

# python -m unittest discover tests