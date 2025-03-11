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
    

    def test_login_cutomer(self):
        credentials = {
            "email": "jane@email.com",
            "password": "1234"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        return response.json['token']
    

    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid email or password')

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
    
    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "phone": "123-456-7890",
            "password": "123"       
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['email'], ['Missing data for required field.'])
    
    def test_get_customers(self):
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], "Jane Doe")
    
    def test_update_customers(self):
        customer_payload = {
        "name": "Johnathan Doe",
        "email": "john@email.com",
        "phone": "3337772222",
        "password": "1234"
        }

        headers = {'Authorization': "Bearer " + self.test_login_cutomer()}

        response = self.client.put('/customers/', json=customer_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Johnathan Doe")

    def test_delete_customers(self):
        headers = {'Authorization': "Bearer " + self.test_login_cutomer()}
        response = self.client.delete('/customers/', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Successfully deleted customer', response.json.get('message', ''))

    
    def test_search_customer(self):
        # Add a few customers for testing search function
        with self.app.app_context():
            db.session.add_all([
                Customer(name="Bill Smith", email="jane@gmail.com", phone="1112223333", password='1234'),
                Customer(name="John Doe", email="john@email.com", phone="3337772222", password='1234'),
                Customer(name="Janet Barney", email="janet@email.com", phone="4445556666", password='1234')
            ])
            db.session.commit()

        response = self.client.get('/customers/search?name=Bill')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'Bill Smith')

        # Testing search with pagination
        response = self.client.get('/customers/search?name=J&page=1&per_page=5')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        self.assertTrue(any(customer['name'] == 'Janet Barney' for customer in response.json))
        self.assertTrue(any(customer['name'] == 'John Doe' for customer in response.json))

        # Testing search with nothing found
        response = self.client.get('/customers/search?name=NonExistent')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)

# python -m unittest discover tests