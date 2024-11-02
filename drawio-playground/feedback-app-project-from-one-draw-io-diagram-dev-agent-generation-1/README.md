# Serverless Feedback Application

This is a serverless application for collecting and managing feedback using AWS services.

## Architecture

The application consists of the following components:

1. API Gateway: Handles incoming HTTP requests.
2. Lambda Function: Processes requests, stores feedback, and sends notifications.
3. DynamoDB Table: Stores the submitted feedback.
4. SNS Topic: Sends notifications when new feedback is received.

## Deployment

To deploy this application:

1. Ensure you have the AWS SAM CLI installed and configured.
2. Navigate to the project directory.
3. Run the following commands:

```bash
sam build
sam deploy --guided
```

Follow the prompts to complete the deployment.

## Usage

After deployment, you will receive an API Gateway URL. You can access the feedback form by opening this URL in a web browser.

To submit feedback:
1. Fill out the feedback form on the landing page.
2. Click the "Submit Feedback" button.
3. You will receive a confirmation message upon successful submission.

## Development

The main application logic is in `app/main.py`. To make changes:

1. Modify the code in `app/main.py`.
2. Update the `template.yaml` file if you've added new resources or changed existing ones.
3. Rebuild and redeploy the application using the SAM CLI commands mentioned above.

## Monitoring

You can monitor the application using AWS CloudWatch. Logs for the Lambda function will be available in the CloudWatch Logs console.