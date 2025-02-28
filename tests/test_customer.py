from app import create_app
from app.models import db, Customer
import unittest

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Adding a customer for use during GET, PUT, and DELETE tests.
            customer = Customer(
                name="Jane Doe",
                email="jane@email.com",
                phone="1112223333",
                password="1234"
            )
            db.session.add(customer)
            db.session.commit()

        self.client = self.app.test_client()
    
    def test_create_customer(self):
        customer_payload = {
        "name": "John Doe",
        "email": "john@email.com",
        "phone": "3337772222",
        "password": "1234"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "John Doe")
    
    def test_get_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], "Jane Doe")
