import unittest
from unittest.mock import patch, MagicMock
from functions.get_visitor_count import main
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()
ALLOWED_ORIGIN = os.getenv('ALLOWED_ORIGIN', 'default_origin_if_not_set')

class TestGetVisitorCount(unittest.TestCase):

    @patch('google.cloud.firestore.Client')
    def test_get_visitor_count_document_exists(self, mock_client):
        # Mock Firestore client
        mock_request = MagicMock(method='GET', headers={'Origin': ALLOWED_ORIGIN})
        mock_document = MagicMock()
        mock_client.return_value.collection.return_value.document.return_value = mock_document

        # Mock Firestore document snapshot for existing document
        mock_snapshot = MagicMock()
        mock_document.get.return_value = mock_snapshot
        mock_snapshot.exists = True
        mock_snapshot.to_dict.return_value = {'count': 10}

        app = Flask(__name__)

        with app.app_context():
            response_data, status_code, headers = main.get_visitor_count(mock_request)

        # Assert the response for an existing document
        self.assertEqual(status_code, 200)
        self.assertIn('counter_value', response_data.json)
        self.assertEqual(response_data.json['counter_value'], 10)

    @patch('google.cloud.firestore.Client')
    def test_get_visitor_count_document_not_exists(self, mock_client):
        # Mock Firestore client
        mock_request = MagicMock(method='GET', headers={'Origin': ALLOWED_ORIGIN})
        mock_document = MagicMock()
        mock_client.return_value.collection.return_value.document.return_value = mock_document

        # Mock Firestore document snapshot for non-existing document
        mock_snapshot = MagicMock()
        mock_document.get.return_value = mock_snapshot
        mock_snapshot.exists = False

        app = Flask(__name__)

        with app.app_context():
            response_data, status_code, headers = main.get_visitor_count(mock_request)

        # Assert the response for a non-existing document
        self.assertEqual(status_code, 404)
        self.assertIn('error', response_data.json)
        self.assertEqual(response_data.json['error'], 'Document not found')

if __name__ == '__main__':
    unittest.main()
