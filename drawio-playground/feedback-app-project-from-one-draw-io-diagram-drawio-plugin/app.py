import json
import boto3
import os
import uuid
from datetime import datetime
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def landing_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Feedback Form</title>
        <script>
            function submitForm(event) {
                event.preventDefault();
                
                const formData = {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    feedback: document.getElementById('feedback').value
                };

                fetch('/Prod/feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Error submitting feedback');
                });
            }
        </script>
    </head>
    <body>
        <h1>Feedback Form</h1>
        <form onsubmit="submitForm(event)">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required><br><br>
            
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required><br><br>
            
            <label for="feedback">Feedback:</label><br>
            <textarea id="feedback" name="feedback" rows="4" cols="50" required></textarea><br><br>
            
            <input type="submit" value="Submit Feedback">
        </form>
    </body>
    </html>
    """
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': html_content
    }

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        return landing_page()
    elif event['httpMethod'] == 'POST':
        try:
            body = json.loads(event['body'])
            
            # Input validation
            required_fields = ['name', 'email', 'feedback']
            for field in required_fields:
                if field not in body or not body[field]:
                    return {
                        'statusCode': 400,
                        'body': json.dumps({'error': f'Missing required field: {field}'})
                    }
            
            feedback = {
                'id': str(uuid.uuid4()),
                'name': body['name'],
                'email': body['email'],
                'feedback': body['feedback'],
                'timestamp': datetime.now().isoformat()
            }
            
            record_feedback(feedback)
            send_confirmation(body['email'])
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Credentials': True,
                },
                'body': json.dumps({'message': 'Feedback submitted successfully'})
            }
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid JSON in request body'})
            }
        except Exception as e:
            print(f"Error: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps({'error': 'Internal server error'})
            }
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }

def record_feedback(feedback):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    try:
        table.put_item(Item=feedback)
    except ClientError as e:
        print(f"Error recording feedback: {e.response['Error']['Message']}")
        raise

def send_confirmation(email):
    topic_arn = os.environ['SNS_TOPIC_ARN']
    message = f"Thank you for your feedback! We have received your submission."
    try:
        sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject="Feedback Confirmation",
            MessageAttributes={
                'email': {
                    'DataType': 'String',
                    'StringValue': email
                }
            }
        )
    except ClientError as e:
        print(f"Error sending confirmation: {e.response['Error']['Message']}")
        raise