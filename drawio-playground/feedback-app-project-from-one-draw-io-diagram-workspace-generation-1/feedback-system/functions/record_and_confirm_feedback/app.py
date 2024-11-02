import json
import boto3
import os
import uuid
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

TABLE_NAME = os.environ['TABLE_NAME']
TOPIC_ARN = os.environ['TOPIC_ARN']

def lambda_handler(event, context):
    try:
        # Parse the incoming request
        body = json.loads(event['body'])
        name = body['name']
        email = body['email']
        feedback = body['feedback']
        
        # Generate a unique ID for the feedback
        feedback_id = str(uuid.uuid4())
        
        # Store the feedback in DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(
            Item={
                'id': feedback_id,
                'name': name,
                'email': email,
                'feedback': feedback
            }
        )
        
        # Publish a message to SNS
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject='New Feedback Received',
            Message=f"New feedback received from {name} ({email}):\n\n{feedback}"
        )
        
        # Send a confirmation email (this is simplified, you might want to use SES for actual email sending)
        confirmation_message = f"Thank you for your feedback, {name}! We have received your message and will review it shortly."
        sns.publish(
            TopicArn=TOPIC_ARN,
            Subject='Feedback Confirmation',
            Message=confirmation_message
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Feedback submitted successfully!')
        }
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps('Error submitting feedback')
        }
