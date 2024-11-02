import json
import unittest
from unittest.mock import patch, MagicMock
from app import lambda_handler, landing_page, record_and_confirm_feedback

class TestApp(unittest.TestCase):

    @patch('app.landing_page')
    def test_lambda_handler_get(self, mock_landing_page):
        mock_landing_page.return_value = {'statusCode': 200, 'body': 'HTML content'}
        event = {'httpMethod': 'GET'}
        result = lambda_handler(event, None)
        self.assertEqual(result['statusCode'], 200)

    @patch('app.record_and_confirm_feedback')
    def test_lambda_handler_post(self, mock_record):
        mock_record.return_value = {'statusCode': 200, 'body': json.dumps('Success')}
        event = {'httpMethod': 'POST', 'body': json.dumps({'name': 'Test', 'email': 'test@example.com', 'feedback': 'Great!'})}
        result = lambda_handler(event, None)
        self.assertEqual(result['statusCode'], 200)

    def test_landing_page(self):
        result = landing_page()
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('text/html', result['headers']['Content-Type'])

    @patch('app.table.put_item')
    @patch('app.send_confirmation')
    def test_record_and_confirm_feedback(self, mock_send_confirmation, mock_put_item):
        feedback = {'name': 'Test', 'email': 'test@example.com', 'feedback': 'Great!'}
        result = record_and_confirm_feedback(feedback)
        self.assertEqual(result['statusCode'], 200)
        mock_put_item.assert_called_once()
        mock_send_confirmation.assert_called_once_with('test@example.com')

if __name__ == '__main__':
    unittest.main()