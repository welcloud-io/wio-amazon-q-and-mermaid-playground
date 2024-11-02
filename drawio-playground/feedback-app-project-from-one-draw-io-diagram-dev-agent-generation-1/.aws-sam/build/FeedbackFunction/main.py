import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        return landing_page()
    elif event['httpMethod'] == 'POST':
        return record_and_confirm_feedback(event, context)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method Not Allowed'})
        }

def landing_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Feedback Form</title>
    </head>
    <body>
        <h1>Feedback Form</h1>
        <form id="feedbackForm">
            <label for="feedback">Your Feedback:</label><br>
            <textarea id="feedback" name="feedback" rows="4" cols="50" required></textarea><br>
            <input type="submit" value="Submit Feedback">
        </form>
        <script>
            document.getElementById('feedbackForm').addEventListener('submit', function(e) {
                e.preventDefault();
                const feedback = document.getElementById('feedback').value;
                fetch('', {
                    method: 'POST',
                    body: JSON.stringify({feedback: feedback}),
                    headers: {'Content-Type': 'application/json'}
                })
                .then(response => response.json())
                .then(data => alert(data.message))
                .catch(error => console.error('Error:', error));
            });
        </script>
    </body>
    </html>
    """
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': html_content
    }

def record_and_confirm_feedback(event, context):
    try:
        feedback = json.loads(event['body'])['feedback']
        
        # Store feedback in DynamoDB
        table = dynamodb.Table(os.environ['FEEDBACK_TABLE'])
        response = table.put_item(Item={'id': context.aws_request_id, 'feedback': feedback})
        
        # Publish to SNS topic
        sns.publish(
            TopicArn=os.environ['FEEDBACK_TOPIC'],
            Message=f'New feedback received: {feedback}'
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Feedback submitted successfully!'})
        }
    except ClientError as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'An error occurred while processing your request.'})
        }
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Missing feedback in request body'})
        }