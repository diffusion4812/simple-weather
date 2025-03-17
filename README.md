# Simple Weather
A weather service hosted on AWS with static and dynamic (API) content.

## Introduction
After experimentation with several AWS services, a serverless implementation was selected based on:
- AWS API Gateway
- AWS S3
- AWS Lambda

### AWS API Gateway
- Handles access requests (is the main URL for client requests).
- Manages rate limiting and throttling
- Enables deployment of muiltiple stages with authentication features for development builds

### AWS S3
- Hosts static content

### AWS Lambda
- Handles and interprets API access requests
- Formats and returns requested information to clients
