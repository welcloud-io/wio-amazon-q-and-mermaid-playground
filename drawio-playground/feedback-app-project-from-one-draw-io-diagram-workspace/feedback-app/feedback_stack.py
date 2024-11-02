# feedback-app/feedback_stack.py

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_dynamodb as dynamodb,
    aws_sns as sns,
    RemovalPolicy
)
from constructs import Construct

class FeedbackStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB table
        feedback_table = dynamodb.Table(
            self, "FeedbackTable",
            partition_key=dynamodb.Attribute(name="email", type=dynamodb.AttributeType.STRING),
            removal_policy=RemovalPolicy.DESTROY
        )

        # Create SNS topic
        feedback_topic = sns.Topic(
            self, "FeedbackTopic",
            display_name="Feedback Notifications"
        )

        # Create Lambda functions
        landing_page_lambda = _lambda.Function(
            self, "LandingPageFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/landing_page")
        )

        record_feedback_lambda = _lambda.Function(
            self, "RecordFeedbackFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="index.handler",
            code=_lambda.Code.from_asset("lambda/record_and_confirm_feedback"),
            environment={
                "FEEDBACK_TABLE_NAME": feedback_table.table_name,
                "SNS_TOPIC_ARN": feedback_topic.topic_arn
            }
        )

        # Grant permissions
        feedback_table.grant_write_data(record_feedback_lambda)
        feedback_topic.grant_publish(record_feedback_lambda)

        # Create API Gateway
        api = apigw.RestApi(self, "FeedbackApi")

        landing_page_integration = apigw.LambdaIntegration(landing_page_lambda)
        api.root.add_method("GET", landing_page_integration)

        feedback_resource = api.root.add_resource("feedback")
        feedback_integration = apigw.LambdaIntegration(record_feedback_lambda)
        feedback_resource.add_method("POST", feedback_integration)
