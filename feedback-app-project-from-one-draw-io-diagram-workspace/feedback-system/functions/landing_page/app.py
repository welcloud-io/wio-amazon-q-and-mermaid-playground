import json

def lambda_handler(event, context):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Feedback Form</title>
        <script>
            function submitForm(e) {
                e.preventDefault();
                
                const formData = {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value, 
                    feedback: document.getElementById('feedback').value
                };

                fetch('/Prod/feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                    alert('Feedback submitted successfully!');
                })
                .catch((error) => {
                    console.error('Error:', error);
                    alert('Error submitting feedback');
                });
            }
        </script>
    </head>
    <body>
        <h1>Feedback Form</h1>
        <form onsubmit="submitForm(event)">
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

