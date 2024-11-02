# feedback-app/tests/test_record_and_confirm_feedback.py

import unittest
from unittest.mock import patch, MagicMock
from _lambda.record_and_confirm_feedback.index import handler

class TestRecordAndConfirmFeedback(unittest.TestCase):
    @patch('boto3.resource')
    @patch('boto3.client')
    def test_handler_success(self, mock_sns_client, mock_dynamodb_resource):
        # Mock DynamoDB and SNS
        mock_table = MagicMock()
        mock_dynamodb_resource.return_value.Table.return_value = mock_table
        mock_sns_client.return_value.publish = MagicMock()

        event = {
            'body': '{"name": "Test User", "email": "test@example.com", "feedback": "Great service!"}'
        }
        context = {}

        result = handler(event, context)

        self.assertEqual(result['statusCode'], 200)
        self.assertIn('Feedback recorded successfully', result['body'])

        # Verify DynamoDB and SNS calls
        mock_table.put_item.assert_called_once()
        mock_sns_client.return_value.publish.assert_called_once()

    @patch('boto3.resource')
    @patch('boto3.client')
    def test_handler_error(self, mock_sns_client, mock_dynamodb_resource):
        # Simulate an error
        mock_dynamodb_resource.return_value.Table.return_value.put_item.side_effect = Exception("Test error")

        event = {
            'body': '{"name": "Test User", "email": "test@example.com", "feedback": "Great service!"}'
        }
        context = {}

        result = handler(event, context)

        self.assertEqual(result['statusCode'], 500)
        self.assertIn('An error occurred', result['body'])

if __name__ == '__main__':
    unittest.main()
