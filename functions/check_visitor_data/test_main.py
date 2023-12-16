import unittest
from unittest.mock import patch, MagicMock
from functions.check_visitor_data import main
from flask import Flask, json

class TestCheckVisitor(unittest.TestCase):

    @patch('google.cloud.firestore.Client')
    def test_check_visitor_by_unique_id(self, mock_client):
        # Mock Firestore client and request
        mock_request = MagicMock(method='POST', get_json=lambda: {'uniqueId': '12345', 'fingerprint': None})
        mock_query_result = MagicMock()
        mock_client.return_value.collection.return_value.where.return_value.limit.return_value.get.return_value = [mock_query_result]

        app = Flask(__name__)

        with app.app_context():
            response_data, status_code, headers = main.check_visitor(mock_request)

        # Assert response for visitor found by uniqueId
        self.assertEqual(status_code, 200)
        self.assertEqual(response_data.json, {'exists': True, 'cookie': '12345'})

    @patch('google.cloud.firestore.Client')
    def test_check_visitor_by_fingerprint(self, mock_client):
        # Mock Firestore client and request
        mock_request = MagicMock(method='POST', get_json=lambda: {'uniqueId': None, 'fingerprint': 'abc123'})
        mock_query_result = MagicMock()
        mock_query_result.to_dict.return_value = {'cookie': 'cookie_value'}
        mock_client.return_value.collection.return_value.where.return_value.limit.return_value.get.return_value = [mock_query_result]

        app = Flask(__name__)

        with app.app_context():
            response_data, status_code, headers = main.check_visitor(mock_request)

        # Assert response for visitor found by fingerprint
        self.assertEqual(status_code, 200)
        self.assertEqual(response_data.json, {'exists': True, 'cookie': 'cookie_value'})

    @patch('google.cloud.firestore.Client')
    def test_check_visitor_not_found(self, mock_client):
        # Mock Firestore client and request
        mock_request = MagicMock(method='POST', get_json=lambda: {'uniqueId': None, 'fingerprint': None})
        mock_client.return_value.collection.return_value.where.return_value.limit.return_value.get.return_value = []

        app = Flask(__name__)

        with app.app_context():
            response_data, status_code, headers = main.check_visitor(mock_request)

        # Assert response for visitor not found
        self.assertEqual(status_code, 200)
        self.assertEqual(response_data.json, {'exists': False})

if __name__ == '__main__':
    unittest.main()
