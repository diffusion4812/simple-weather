import json, os, logging, boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('wx-serv-data')

logger = logging.getLogger()
log_level = os.environ.get('LOG_LEVEL', 'INFO')
logger.setLevel(log_level)

def get_temperature(lon, lat):
    response_content = json.dumps({'temperature': str("{:0.5f}".format(25.0))})
    response_code = '200'
    return response_content, response_code

def get_windspeed(lon, lat):
    response_content = json.dumps({'message': 'valid longitude and latitude provided'})
    response_code = '200'
    return response_content, response_code

def get_humidity(lon, lat):
    response_content = json.dumps({'message': 'valid longitude and latitude provided'})
    response_code = '200'
    return response_content, response_code

def get_pressure(lon, lat):
    response_content = json.dumps({'message': 'valid longitude and latitude provided'})
    response_code = '200'
    return response_content, response_code

api_endpoints = {'/api/temperature': get_temperature,
                 '/api/windspeed': get_windspeed,
                 '/api/humidity': get_humidity,
                 '/api/pressure': get_pressure}

def run_api_query(path, querystring):
    if querystring.get('lon') and querystring.get('lat'):
        response_content, response_code = api_endpoints[path](querystring['lon'], querystring['lat'])
    else:
        response_content = json.dumps({'message': 'valid longitude and latitude not provided'})
        response_code = '400'

    response = {'body': response_content, 'code': response_code}
    return response

def lambda_handler(event, context):
    if event['path'] in api_endpoints and event['queryStringParameters']:
        response = run_api_query(event['path'], event['queryStringParameters'])
    elif not event['queryStringParameters']:
        response = {
            'body': json.dumps({'message': 'no query parameters provided'}),
            'code': '400'
        }
    else:
        response = {
            'body': json.dumps({'message': 'endpoint not found'}),
            'code': '400'
        }

    results = table.query(
        KeyConditionExpression=Key('station_id').eq('ZVDB')
    )
    items = response.items()

    response['body'] = json.dumps(items)

    return {
        'isBase64Encoded': False,
        'statusCode': int(response['code']),
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': response['body']
    }
