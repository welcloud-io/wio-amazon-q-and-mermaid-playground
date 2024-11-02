import json

def lambda_handler(event, context):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Feedback Form</title>
    </head>
    <body>
        <h1>Feedback Form</h1>
        <form action="/Prod/feedback" method="post">
            <label for="name">Name:</label><br>
            <input type="text" id="name" name="name" required><br>
            <label for="email">Email:</label><br>
            <input type="email" id="email" name="email" required><br>
            <label for="feedback">Feedback:</label><br>
            <textarea id="feedback" name="feedback" required></textarea><br>
            <input type="submit" value="Submit">
        </form>
    </body>
    </html>
    """

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': html_content
    }

