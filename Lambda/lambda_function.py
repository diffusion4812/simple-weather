import json, os, logging

# Initialize the logger
logger = logging.getLogger()

# Get the log level from the environment variable and default to INFO if not set
log_level = os.environ.get('LOG_LEVEL', 'INFO')

# Set the log level
logger.setLevel(log_level)

def lambda_handler(event, context):
    body = json.dumps(event['queryStringParameters'])
    if event['queryStringParameters'].get('lon') and event['queryStringParameters'].get('lat'):
        body = json.dumps({'message':'You requested information for lon={}, lat={}'.format(event['queryStringParameters']['lon'], event['queryStringParameters']['lat'])})
        statusCode = 200
    else:
        body = json.dumps({'message':'You did not provide a valid lon and lat'})
        statusCode = 400
    return {
        'statusCode': statusCode,
        'body': body
    }
