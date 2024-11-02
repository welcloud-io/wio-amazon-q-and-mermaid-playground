ARCHITECT
When asked to generate application code, follow this guidance:
- Use python for the lambda function's code
- Use python AWS CDK V2 for the Infrastructure as Code

When you generate a lambda function, follow this guidance:
- write a unit test case for each lambda function
- isolate html code in a specific file with '.html' extension

When you generate Infrastructure as code with the CDK, follow this guidance:
- seperate the file containing the stack from the app.py file containing app.synth() function
- write relevant CDK unit tests for the component of the stacks 