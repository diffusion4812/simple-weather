import unittest
from Lambda.lambda_function import lambda_handler

# Unit tests for the Lambda function
class TestLambdaHandler(unittest.TestCase):
    # Test case: Valid query parameters with a valid station_id
    def test_valid_query_parameters(self):
        event = {
            'path': '/api/temperature',  # API endpoint for temperature
            'queryStringParameters': {'station_id': 'SILJ'}  # Valid station ID
        }
        context = {}
        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)  # Expect HTTP 200 OK
        self.assertIn('temperature', response['body'])  # Response should include 'temperature'

    # Test case: Missing query parameters (no station_id provided)
    def test_missing_query_parameters(self):
        event = {
            'path': '/api/temperature',  # API endpoint for temperature
            'queryStringParameters': {}  # Empty query parameters
        }
        context = {}
        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 400)  # Expect HTTP 400 Bad Request
        self.assertIn('valid station ID required', response['body'])  # Error message should indicate missing station ID

    # Test case: Invalid API endpoint
    def test_invalid_endpoint(self):
        event = {
            'path': '/api/unknown',  # Invalid API endpoint
            'queryStringParameters': {'station_id': 'SILJ'}  # Valid station ID
        }
        context = {}
        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 400)  # Expect HTTP 400 Bad Request
        self.assertIn('endpoint not found', response['body'])  # Error message should indicate invalid endpoint

# Run the unit tests
if __name__ == '__main__':
    unittest.main()