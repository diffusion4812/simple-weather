import json, os, logging

# Initialize the logger
logger = logging.getLogger()

# Get the log level from the environment variable and default to INFO if not set
log_level = os.environ.get('LOG_LEVEL', 'INFO')

# Set the log level
logger.setLevel(log_level)

def lambda_handler(event, context):
    body = json.dumps(event['queryStringParameters'])

    return {
        'statusCode': 200,
        'body': body
    }
