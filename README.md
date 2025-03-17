Weather service hosted on AWS with static and dynamic (API) content.

Serverless backend utilising:
1. AWS API Gateway
2. AWS S3
3. AWS Lambda

## AWS API Gateway
- Handles access requests (is the main URL for client requests).
- Manages rate limiting and throttling
- Enables deployment of muiltiple stages with authentication features for development builds

## AWS S3
- Hosts static content

## AWS Lambda
- Handles and interprets API access requests
- Formats and returns requested information to clients
