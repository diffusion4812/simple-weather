import json, os, logging

# Initialize the logger
logger = logging.getLogger()

# Get the log level from the environment variable and default to INFO if not set
log_level = os.environ.get('LOG_LEVEL', 'INFO')

# Set the log level
logger.setLevel(log_level)

api_endpoints = ['/api/temperature',
                 '/api/windspeed',
                 '/api/humidity',
                 '/api/pressure']

def run_api_query(querystring):
  if querystring.get('lon') and querystring.get('lat'):
    response_content = json.dumps({'message':'You requested weather information for lon={}, lat={}'.format(querystring['lon'][0], querystring['lat'][0])})
    response_code = '200 OK'
  else:
    response_content = json.dumps({'message':'You did not provide a valid lon and lat'})
    response_code = '400 Bad Request'

  response = {'body': response_content, 'code': response_code}
  return response

def lambda_handler(event, context):
    body = json.dumps(event['queryStringParameters'])

    if event['rawPath'] in api_endpoints:
        response = run_api_query(event['queryStringParameters'])

    return {
        'statusCode': response['code'],
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': response['body']
    }
