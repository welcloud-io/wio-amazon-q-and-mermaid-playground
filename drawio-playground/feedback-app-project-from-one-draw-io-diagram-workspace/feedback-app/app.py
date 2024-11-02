# feedback-app/app.py

#!/usr/bin/env python3
import os
from aws_cdk import App
from feedback_stack import FeedbackStack

app = App()
FeedbackStack(app, "FeedbackStack")
app.synth()
