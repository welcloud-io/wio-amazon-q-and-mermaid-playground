import json
import os
import pytest
from moto import mock_dynamodb, mock_sns
from app import lambda_handler

@pytest.fixture
def aws_credentials():
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
    os.environ['DYNAMODB_TABLE'] = 'FeedbackTable'
    os.environ['SNS_TOPIC_ARN'] = 'arn:aws:sns:us-east-1:123456789012:FeedbackTopic'

@mock_dynamodb
@mock_sns
def test_lambda_handler(aws_credentials):
    event = {
        'body': json.dumps({
            'name': 'Test User',
            'email': 'test@example.com',
            'feedback': 'This is a test feedback'
        })
    }
    context = {}

    response = lambda_handler(event, context)

    assert response['statusCode'] == 200
    assert json.loads(response['body'])['message'] == 'Feedback submitted successfully'

@mock_dynamodb
@mock_sns
def test_lambda_handler_missing_field(aws_credentials):
    event = {
        'body': json.dumps({
            'name': 'Test User',
            'email': 'test@example.com'
            # Missing 'feedback' field
        })
    }
    context = {}

    response = lambda_handler(event, context)

    assert response['statusCode'] == 400
    assert json.loads(response['body'])['error'] == 'Missing required field: feedback'

@mock_dynamodb
@mock_sns
def test_lambda_handler_invalid_json(aws_credentials):
    event = {
        'body': 'This is not valid JSON'
    }
    context = {}

    response = lambda_handler(event, context)

    assert response['statusCode'] == 400
    assert json.loads(response['body'])['error'] == 'Invalid JSON in request body'