# Serverless Feedback Application

This application allows users to submit feedback through a web form and stores the feedback in a DynamoDB table. It also sends a confirmation email to the user using Amazon SNS.

## Prerequisites

- AWS account
- AWS CLI configured with appropriate permissions
- Python 3.8 or later
- Boto3 library

## Deployment Instructions

1. Create a DynamoDB table named "FeedbackTable" with a partition key "email" (String).

2. Create an SNS topic for sending confirmation emails and note the ARN.

3. Update the `YOUR_SNS_TOPIC_ARN` placeholder in `app.py` with your actual SNS topic ARN.

4. Create a Lambda function:
   - Runtime: Python 3.8 or later
   - Handler: app.lambda_handler
   - Upload the `app.py` file as the function code
   - Set the function's execution role to include permissions for DynamoDB and SNS

5. Create an API Gateway:
   - Create a new REST API
   - Create a resource and add GET and POST methods
   - Set the integration type to "Lambda Function" and select your Lambda function
   - Deploy the API

6. Update the form action in the `landing_page()` function with your API Gateway endpoint URL.

## Usage

Access the landing page through your API Gateway endpoint. Users can fill out the feedback form, which will be stored in DynamoDB, and they will receive a confirmation email.

## Troubleshooting

- Check CloudWatch Logs for any error messages from the Lambda function.
- Ensure that the Lambda function has the necessary permissions to access DynamoDB and SNS.
- Verify that the SNS topic ARN is correctly set in the `app.py` file.