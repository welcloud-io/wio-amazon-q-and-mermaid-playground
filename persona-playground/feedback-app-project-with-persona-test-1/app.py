import json
import boto3
from botocore.exceptions import ClientError

import os
import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('DYNAMODB_TABLE', 'FeedbackTable'))
sns = boto3.client('sns')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN', 'YOUR_SNS_TOPIC_ARN')

def lambda_handler(event, context):
    try:
        if event['httpMethod'] == 'GET':
            return landing_page()
        elif event['httpMethod'] == 'POST':
            body = json.loads(event['body'])
            return record_and_confirm_feedback(body)
        else:
            return {
                'statusCode': 405,
                'body': json.dumps('Method Not Allowed')
            }
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Internal Server Error')
        }

def landing_page():
    html_content = """
    <html>
    <body>
        <h1>Feedback Form</h1>
        <form action="" method="post">
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name" required><br>
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email" required><br>
            <label for="feedback">Feedback:</label><br>
            <textarea id="feedback" name="feedback" required></textarea><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': html_content
    }

def record_and_confirm_feedback(feedback):
    if not all(key in feedback for key in ['name', 'email', 'feedback']):
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required fields')
        }
    
    try:
        table.put_item(Item=feedback)
    except ClientError as e:
        print(f"Error recording feedback: {e.response['Error']['Message']}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error recording feedback')
        }

    try:
        send_confirmation(feedback['email'])
    except ClientError as e:
        print(f"Error sending confirmation: {e.response['Error']['Message']}")
        # We still return success to the user even if confirmation fails

    return {
        'statusCode': 200,
        'body': json.dumps('Feedback submitted successfully!')
    }

def send_confirmation(email):
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message='Thank you for your feedback! We have received your submission.',
        Subject='Feedback Confirmation',
        MessageAttributes={
            'email': {
                'DataType': 'String',
                'StringValue': email
            }
        }
    )