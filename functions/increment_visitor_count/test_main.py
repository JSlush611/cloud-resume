import unittest
from unittest.mock import patch, MagicMock
from functions.increment_visitor_count import main
from flask import Flask

class TestIncrementVisitorCount(unittest.TestCase):
    @patch('google.cloud.firestore.Client')
    def test_increment_visitor_count(self, mock_client):
        mock_request = MagicMock()
        mock_transaction = MagicMock()
        mock_client.return_value.transaction.return_value = mock_transaction
        mock_document = MagicMock()
        mock_client.return_value.collection.return_value.document.return_value = mock_document

        mock_snapshot = MagicMock()
        mock_document.get.return_value = mock_snapshot
        mock_snapshot.exists = True
        mock_snapshot.get.return_value = 5  

        app = Flask(__name__)

        with app.app_context():
            response_data, status_code, headers = main.increment_visitor_count(mock_request)

        # Check that Firestore methods were called correctly
        mock_client.return_value.collection.assert_called_with('counters')
        mock_client.return_value.collection.return_value.document.assert_called_with('visitorCount')
        mock_transaction.update.assert_called()  

        self.assertEqual(status_code, 200)
        self.assertIn('updated_count', response_data.json)
        self.assertEqual(response_data.json['updated_count'], 6)  # Expecting count to increment from 5 to 6

if __name__ == '__main__':
    unittest.main()
