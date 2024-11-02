# feedback-app/tests/test_feedback_stack.py

import aws_cdk as core
import aws_cdk.assertions as assertions
from feedback_stack import FeedbackStack

def test_feedback_stack():
    app = core.App()
    stack = FeedbackStack(app, "feedback-stack")
    # template = assertions.Template.from_stack(stack)

    # # template.resource_count_is("AWS::Lambda::Function", 2)

    # template.has_resource_properties("AWS::ApiGateway::RestApi", {
    #     "Name": "FeedbackApi"
    # })

if __name__ == '__main__':
    test_feedback_stack()
