from app import create_app
from app.models import db, Mechanic
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

#TODO create test for get mechanics sorted by most tickets assigned.

# python -m unittest discover tests