# feedback-app/lambda/landing_page/index.py

import json

def handler(event, context):
    with open("index.html", "r") as f:
        html_content = f.read()
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/html"
        },
        "body": html_content
    }
