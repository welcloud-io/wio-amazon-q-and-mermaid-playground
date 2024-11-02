# feedback-app/lambda/record_and_confirm_feedback/index.py

import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

def handler(event, context):
    try:
        # Parse the incoming JSON data
        body = json.loads(event['body'])
        
        # Store the feedback in DynamoDB
        table = dynamodb.Table(os.environ['FEEDBACK_TABLE_NAME'])
        table.put_item(Item={
            'email': body['email'],
            'name': body['name'],
            'feedback': body['feedback']
        })
        
        # Send a notification via SNS
        sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Subject='New Feedback Received',
            Message=f"New feedback received from {body['name']} ({body['email']}):\n\n{body['feedback']}"
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Feedback recorded successfully'})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'An error occurred while processing your feedback'})
        }
