import unittest
from app import app, products_collection
from unittest.mock import patch, MagicMock
from app import app, collection, client
import mongomock

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.products_collection.find')
    def test_products_route(self, mock_find):
        # Mock the MongoDB find method
        mock_find.return_value = [
            {'name': 'Product 1', 'price': 10.99},
            {'name': 'Product 2', 'price': 5.49}
        ]

        response = self.app.get('/products')

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check for presence of product names in the response data
        self.assertIn(b'Product 1', response.data)
        self.assertIn(b'Product 2', response.data)

class MongoDBConnectionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.client')
    def test_ping_db_success(self, mock_client):
        # Mock the ping command to simulate a successful connection
        mock_client.admin.command.return_value = {"ok": 1.0}

        response = self.app.get('/ping_db')

        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'MongoDB connection is successful!', response.data)

    @patch('app.client')
    def test_ping_db_failure(self, mock_client):
        # Mock the ping command to simulate a failed connection
        mock_client.admin.command.side_effect = Exception("Server not available")

        response = self.app.get('/ping_db')

        # Assert that the response indicates a server error
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Server not available', response.data)

class MongoDBWriteOperationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.patcher = patch('app.collection', mongomock.MongoClient().db.collection)
        self.mock_collection = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_add_product(self):
        # Define the product data to be inserted
        product_data = {
            "name": "Test Product",
            "price": 19.99,
            "quantity": 100
        }

        # Send a POST request to the /add_product route
        response = self.app.post('/add_product', json=product_data)

        # Assert that the response status code is 201 Created
        self.assertEqual(response.status_code, 201)

        # Query the database to check if the product was inserted
        inserted_product = self.mock_collection.find_one({"name": "Test Product"})

        # Assert that the inserted product is not None
        self.assertIsNotNone(inserted_product)

        # Assert that the inserted product data matches the original data
        self.assertEqual(inserted_product['name'], product_data['name'])
        self.assertEqual(inserted_product['price'], product_data['price'])
        self.assertEqual(inserted_product['quantity'], product_data['quantity'])


if __name__ == '__main__':
    unittest.main()
