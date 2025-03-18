<style>
h4:has(+ ul) {
  margin-bottom: 0.2em;
}
h4 + ul {
  margin-top: 0.2em;
}
p {
  text-align: justify
}
img {
    display: block;
    margin: auto;
}
</style>

# Simple Weather
A weather service hosted on AWS with static and dynamic (API) content.

## Introduction
After experimentation with several AWS services, a serverless implementation was selected based on:
- AWS API Gateway
- AWS S3
- AWS Lambda

#### AWS API Gateway
- Handles access requests (is the main URL for client requests), routing them to the appropriate AWS service.
- Manages rate limiting and throttling.
- Enables deployment of muiltiple stages with authentication features for development builds.

#### AWS S3
- Hosts static content like HTML, CSS and JavaScript.

#### AWS Lambda
- Handles and interprets API access requests.
- Formats and returns requested information to clients.


## AWS API Gateway
Four resources have been defined to handle hosting of static content and proper fielding of API requests (through AWS Lambda).

~~~
/             - Usage webpage
/{proxy+}     - Usage webpage (supporting files)
/api          - API root (redirects to usage webpage)
/api/{proxy+} - Weather API
~~~

Methods within API Gateway resources are defined to handle **only** GET requests. Any other request will be denied.

~~~
/             - GET → AWS integration with S3
/{proxy+}     - GET → AWS integration with S3
/api          - GET → Mock integration (internal)
/api/{proxy+} - GET → Lambda integration
~~~

## Frontend
Static HTML content is hosted in an AWS S3 bucket. Because the API Gateway is used to route GET requests to AWS S3, public access to the bucket can remain disabled for enhanced security.

The Chromium DevTools suite (in Microsoft Edge) was a crucial design aid for debugging, testing and supporting design decisions made as part of the frontend application design.

## Backend
Any requests to `/api` endpoints are routed to an AWS Lambda function running Python. This function interacts with a DynamoDB instance

## Testing
Testing took the form of several guises during project development. Compared to running applications locally, cloud hosting introduces additional delays related to uploading code and any requirement for re-provisioning resources for the service provider.

### Local Hosting
asd

### Automated Testing
asd

### Data Synthesizing
As the collation of live weather data was not feasible, an AWS Lambda utility function was created to populate the DynamoDB `wx-serv-data` table with synthetic data. It was important to test the application with 

## Future Improvements and Known Issues

### Weather Stations
Weather stations are currently hard-coded in the frontend and backend applications. This could become difficult to maintain if the quantity of data-providers is expected to change.

### Database Edge Cases
Currently, API requests with empty database tables are likely to crash the application (AWS Lambda function). Checks should be added to ensure the validity and existence of data in database tables.