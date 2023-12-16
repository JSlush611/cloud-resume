import unittest
from unittest.mock import patch, MagicMock
from functions.add_visitor import main
from flask import Flask

class TestAddVisitor(unittest.TestCase):

    @patch('google.cloud.firestore.Client')
    def test_add_visitor(self, mock_client):
        # Mock Firestore client and request
        mock_request = MagicMock(method='POST', get_json=lambda: {'cookie': 'test_cookie', 'fingerprint': 'test_fingerprint'})
        mock_collection = MagicMock()
        mock_client.return_value.collection.return_value = mock_collection

        app = Flask(__name__)

        with app.app_context():
            response_data, status_code, headers = main.add_visitor(mock_request)

        # Assert that Firestore methods were called correctly
        mock_client.return_value.collection.assert_called_with('visitors')
        
        # Check if 'add' was called and if the provided dictionary contains the expected keys
        mock_collection.add.assert_called()
        args, _ = mock_collection.add.call_args
        self.assertIn('cookie', args[0])
        self.assertIn('fingerprint', args[0])
        self.assertIn('timestamp', args[0])

        # Assert the response
        self.assertEqual(status_code, 200)
        self.assertEqual(response_data.json, {'status': 'success'})

if __name__ == '__main__':
    unittest.main()
