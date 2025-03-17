import json, os, logging, boto3
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)

dynamodb = boto3.resource('dynamodb')
data_table = dynamodb.Table('wx-serv-data')
stations_table = dynamodb.Table('wx-serv-stations')

lambda_populate = boto3.client('lambda')

logger = logging.getLogger()
log_level = os.environ.get('LOG_LEVEL', 'INFO')
logger.setLevel(log_level)

def get_record(station_id):
    response = data_table.query(
        KeyConditionExpression=Key('station_id').eq(station_id),
        ScanIndexForward=False,
        Limit=1
    )
    return json.loads(json.dumps(response['Items'], cls=DecimalEncoder))

def get_temperature(station_id):
    response_content = json.dumps({'temperature': get_record(station_id)[0]['temperature']})
    response_code = '200'
    return response_content, response_code

def get_windspeed(station_id):
    response_content = json.dumps({'speed': get_record(station_id)[0]['windspeed']['speed'],
                                   'bearing': get_record(station_id)[0]['windspeed']['bearing']})
    response_code = '200'
    return response_content, response_code

def get_humidity(station_id):
    response_content = json.dumps({'temperature': get_record(station_id)[0]['humidity']})
    response_code = '200'
    return response_content, response_code

def get_pressure(station_id):
    response_content = json.dumps({'temperature': get_record(station_id)[0]['pressure']})
    response_code = '200'
    return response_content, response_code

api_endpoints = {'/api/temperature': get_temperature,
                 '/api/windspeed': get_windspeed,
                 '/api/humidity': get_humidity,
                 '/api/pressure': get_pressure}

def run_api_query(path, querystring):
    if querystring.get('station_id'):
        response_content, response_code = api_endpoints[path](querystring['station_id'])
    else:
        response_content = json.dumps({'message': 'valid station ID required'})
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

    lambda_populate.invoke(FunctionName="wx-serv-populate",
                            InvocationType='Event',
                            Payload='{}')

    return {
        'isBase64Encoded': False,
        'statusCode': int(response['code']),
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': response['body']
    }
