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
- Handles access requests (is the main URL for client requests).
- Manages rate limiting and throttling
- Enables deployment of muiltiple stages with authentication features for development builds

#### AWS S3
- Hosts static content

#### AWS Lambda
- Handles and interprets API access requests
- Formats and returns requested information to clients


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
/             - GET
/{proxy+}     - GET
/api          - GET
/api/{proxy+} - GET
~~~

