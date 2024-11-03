# Feedback Application

This application allows users to submit feedback, which is then stored in a DynamoDB table and triggers an SNS notification.

## Setup

1. Install the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
2. Clone this repository
3. Navigate to the project directory
4. Run `sam build` to build the application
5. Run `sam deploy --guided` to deploy the application
   - Follow the prompts to configure the deployment
   - When asked about functions that may not have authorization defined, confirm that you want to deploy

## Usage

Send a POST request to the API Gateway endpoint with JSON payload containing feedback information.

### API Endpoint

After deployment, the API endpoint URL will be displayed in the outputs. You can also find it in the AWS Console under API Gateway.

### Request Format

Send a POST request to the API endpoint with the following JSON payload:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "feedback": "Great service!"
}
```

### Response

- Successful submission (HTTP 200):
  ```json
  {
    "message": "Feedback submitted successfully"
  }
  ```

- Error responses:
  - Missing required field (HTTP 400):
    ```json
    {
      "error": "Missing required field: [field_name]"
    }
    ```
  - Invalid JSON (HTTP 400):
    ```json
    {
      "error": "Invalid JSON in request body"
    }
    ```
  - Internal server error (HTTP 500):
    ```json
    {
      "error": "Internal server error"
    }
    ```

## Architecture

The application uses the following AWS services:
- AWS Lambda: Processes the feedback submission
- Amazon API Gateway: Provides the HTTP endpoint for submitting feedback
- Amazon DynamoDB: Stores the feedback data
- Amazon SNS: Sends confirmation emails

## Monitoring and Logs

You can monitor the application and view logs in the AWS Console:
- Use CloudWatch Logs to view Lambda function logs
- Use DynamoDB tables to view stored feedback
- Use SNS to manage email subscriptions and view message delivery status

## Local Development

To run the application locally for development:

1. Install [Docker](https://www.docker.com/get-started)
2. Run `sam local start-api`
3. The API will be available at `http://localhost:3000`

## Running Tests

To run unit tests:

1. Install development dependencies: `pip install -r requirements-dev.txt`
2. Run tests: `pytest tests/`

## Cleanup

To remove the application and all associated resources from your AWS account:

1. Run `sam delete`
2. Confirm the deletion when prompted

This will delete all resources created by the SAM template, including the Lambda function, API Gateway, DynamoDB table, and SNS topic.