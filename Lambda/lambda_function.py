import json, os, logging, boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

# Custom JSON encoder to handle DynamoDB Decimal type
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)  # Convert Decimal to string for JSON serialization
        return super().default(obj)

# Initialize DynamoDB resources
dynamodb = boto3.resource('dynamodb')
data_table = dynamodb.Table('wx-serv-data')  # Table storing weather data
stations_table = dynamodb.Table('wx-serv-stations')  # (Optional) Table for station metadata

# Initialize AWS Lambda client for invoking other Lambda functions
lambda_populate = boto3.client('lambda')

# Set up logging
logger = logging.getLogger()
log_level = os.environ.get('LOG_LEVEL', 'INFO')  # Default log level is INFO
logger.setLevel(log_level)

# Function to query the latest weather record for a given station ID
def get_record(station_id):
    response = data_table.query(
        KeyConditionExpression=Key('station_id').eq(station_id),  # Filter by station_id
        ScanIndexForward=False,  # Retrieve the latest record (descending order)
        Limit=1  # Limit to one record
    )
    # Convert DynamoDB response to JSON-compatible format
    return json.loads(json.dumps(response['Items'], cls=DecimalEncoder))

# API endpoint handlers for different types of weather data

# Retrieve temperature data
def get_temperature(station_id):
    response_content = json.dumps({'temperature': get_record(station_id)[0]['temperature']})
    response_code = '200'
    return response_content, response_code

# Retrieve wind speed and bearing data
def get_windspeed(station_id):
    response_content = json.dumps({'speed': get_record(station_id)[0]['windspeed']['speed'],
                                   'bearing': get_record(station_id)[0]['windspeed']['bearing']})
    response_code = '200'
    return response_content, response_code

# Retrieve humidity data
def get_humidity(station_id):
    response_content = json.dumps({'humidity': get_record(station_id)[0]['humidity']})
    response_code = '200'
    return response_content, response_code

# Retrieve pressure data
def get_pressure(station_id):
    response_content = json.dumps({'pressure': get_record(station_id)[0]['pressure']})
    response_code = '200'
    return response_content, response_code

# Map API paths to their respective handler functions
api_endpoints = {
    '/api/temperature': get_temperature,
    '/api/windspeed': get_windspeed,
    '/api/humidity': get_humidity,
    '/api/pressure': get_pressure
}

# Validate and process API queries
def run_api_query(path, querystring):
    if querystring.get('station_id'):  # Check if station_id is provided
        # Lookup and call the appropriate endpoint handler
        response_content, response_code = api_endpoints[path](querystring['station_id'])
    else:
        # Return error if station_id is missing
        response_content = json.dumps({'message': 'valid station ID required'})
        response_code = '400'

    # Construct the response
    response = {'body': response_content, 'code': response_code}
    return response

# Main Lambda handler function (AWS)
def lambda_handler(event, context):
    # Check if the requested path is valid and querystring parameters are provided
    if event['path'] in api_endpoints and event['queryStringParameters']:
        response = run_api_query(event['path'], event['queryStringParameters'])
    elif not event['queryStringParameters']:
        # Handle missing querystring parameters
        response = {
            'body': json.dumps({'message': 'no query parameters provided'}),
            'code': '400'
        }
    else:
        # Handle invalid API paths
        response = {
            'body': json.dumps({'message': 'endpoint not found'}),
            'code': '400'
        }

    # Asynchronously invoke the data population Lambda function
    lambda_populate.invoke(
        FunctionName="wx-serv-populate",
        InvocationType='Event',  # Fire-and-forget invocation
        Payload='{}'
    )

    # Return the final response to the client
    return {
        'isBase64Encoded': False,
        'statusCode': int(response['code']),
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': response['body']
    }
