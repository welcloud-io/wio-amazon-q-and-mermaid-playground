# feedback-app/tests/test_landing_page.py

import unittest
from unittest.mock import patch, mock_open
from _lambda.landing_page.index import handler

class TestLandingPage(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="<html>Test Content</html>")
    def test_handler(self, mock_file):
        event = {}
        context = {}
        result = handler(event, context)
        
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'text/html')
        self.assertEqual(result['body'], "<html>Test Content</html>")

if __name__ == '__main__':
    unittest.main()
