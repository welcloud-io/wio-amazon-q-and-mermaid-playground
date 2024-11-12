from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
)
from constructs import Construct

class ServerlessCrudStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create DynamoDB table
        table = dynamodb.Table(
            self, "ItemsTable",
            partition_key=dynamodb.Attribute(
                name="id",
                type=dynamodb.AttributeType.STRING
            )
        )

        # Create Lambda function
        crud_lambda = lambda_.Function(
            self, "CrudFunction",
            runtime=lambda_.Runtime.RUBY_2_7,
            handler="index.handler",
            code=lambda_.Code.from_asset("lambda"),
            environment={
                "TABLE_NAME": table.table_name
            }
        )

        # Grant Lambda function read/write permissions to DynamoDB table
        table.grant_read_write_data(crud_lambda)

        # Create API Gateway
        api = apigateway.RestApi(
            self, "CrudApi",
            rest_api_name="Serverless CRUD API",
            description="This service serves a serverless CRUD API."
        )

        crud_integration = apigateway.LambdaIntegration(crud_lambda)

        items = api.root.add_resource("items")
        items.add_method("GET", crud_integration)  # GET /items
        items.add_method("POST", crud_integration)  # POST /items

        item = items.add_resource("{id}")
        item.add_method("GET", crud_integration)  # GET /items/{id}
        item.add_method("PUT", crud_integration)  # PUT /items/{id}
        item.add_method("DELETE", crud_integration)  # DELETE /items/{id}

