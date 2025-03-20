import unittest
from Lambda.lambda_function import lambda_handler

class TestLambdaHandler(unittest.TestCase):
    def test_valid_query_parameters(self):
        event = {
            'path': '/api/temperature',
            'queryStringParameters': {'station_id': 'SILJ'}
        }
        context = {}
        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('temperature', response['body'])

    def test_missing_query_parameters(self):
        event = {
            'path': '/api/temperature',
            'queryStringParameters': {}
        }
        context = {}
        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('valid station ID required', response['body'])

    def test_invalid_endpoint(self):
        event = {
            'path': '/api/unknown',
            'queryStringParameters': {'station_id': 'SILJ'}
        }
        context = {}
        response = lambda_handler(event, context)
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('endpoint not found', response['body'])

if __name__ == '__main__':
    unittest.main()