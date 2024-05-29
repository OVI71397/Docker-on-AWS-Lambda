# Data Collection

## Objective
Create an automatic pipeline that will be collecting traveling data from open-source API. 

## Implementation
The Python script lambda_function.py makes API requests and preprocesses the raw data to produce CSV file, which is then stored in an AWS S3 bucket. 
The script and its dependencies are packed with a Docker container and pushed to Amazon Elastic Container Service. 
The container is further deployed on the AWS Lambda function and scheduled for automatic execution with Amazon CloudWatch.

## Features

- **Automated Data Collection**: Regularly fetches travel data from an open-source API.
- **Data Preprocessing**: Cleans and preprocesses the raw data into a structured CSV format.
- **AWS Integration**: Uses AWS Lambda for serverless execution, AWS S3 for data storage, and Amazon ECS for container management.
- **Scheduled Execution**: Employs Amazon CloudWatch to automate the Lambda function calls at regular intervals.


 **AWS Services**:
  - AWS Lambda
  - Amazon S3
  - Amazon ECS
  - Amazon CloudWatch
