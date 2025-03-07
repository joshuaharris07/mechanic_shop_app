from app import create_app
from app.models import db, Inventory
import unittest

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            # Adding a part for use during GET, PUT, and DELETE tests.
            part = Inventory(
                name="Front Bumper",
                price=139.50
            )
            db.session.add(part)
            db.session.commit()

        self.client = self.app.test_client()
    
    def test_create_part(self):
        part_payload = {
        "name": "Windshield Wipers",
        "price": 21.75
        }

        response = self.client.post('/inventory/', json=part_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Windshield Wipers")
    
    def test_get_inventory(self):
        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], "Front Bumper")

    def test_update_part(self): 
        update_payload = {
            "name": "Rear Bumper"
        }

        response = self.client.put('/inventory/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Rear Bumper') 
        self.assertEqual(response.json['price'], 139.50)

    def test_update_part2(self): 
        update_payload = {
            "price": 205.49
        }

        response = self.client.put('/inventory/1', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Front Bumper') 
        self.assertEqual(response.json['price'], 205.49)
    
    def test_delete_part(self):
        response = self.client.delete('/inventory/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Part was successfully deleted', response.json.get('message', ''))
    
    def test_delete_nonexistent_part(self):
        response = self.client.delete('/inventory/2')
        self.assertEqual(response.status_code, 404)

# python -m unittest discover tests