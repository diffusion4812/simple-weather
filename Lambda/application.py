import logging.handlers, urllib.parse, json

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Handler 
LOG_FILE = 'weather-service.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add Formatter to Handler
handler.setFormatter(formatter)

# add Handler to Logger
logger.addHandler(handler)

usage_file = open('statichtml/usage.html', 'r')
usage = usage_file.read()
usage_file.close()

api_endpoints = ['temperature', 'windspeed', 'humidity', 'pressure']

def run_api_query(query_string):
  query = urllib.parse.parse_qs(query_string)
  if query.get('lon') and query.get('lat'):
    response_content = json.dumps({'message':'You requested weather information for lon={}, lat={}'.format(query['lon'][0], query['lat'][0])})
    response_code = '200 OK'
  else:
    response_content = json.dumps({'message':'You did not provide a valid lon and lat'})
    response_code = '400 Bad Request'

  response = {'content': response_content, 'type': 'application/json', 'code': response_code}
  return response

def application(environ, start_response):
  response = {'content': '', 'type': '', 'code': ''}
  path = environ['PATH_INFO'].split('/')
  for i in range(len(path)):
    path[i] = urllib.parse.unquote_plus(path[i])

  if environ['REQUEST_METHOD'] == 'GET':
    if path[1] == '':
      response['content'] = usage
      response['code'] = '200 OK'
      response['type'] = 'text/html'
    elif path[1] == 'api' and len(path) > 2:
      if path[2] in api_endpoints:
        response = run_api_query(environ['QUERY_STRING'])
      else:
        response['content'] = json.dumps({'message':'Invalid API endpoint'}) 
        response['code'] = '404 Not Found'
        response['type'] = 'application/json'
    else:
      response['content'] = '<meta http-equiv="refresh" content="0; url=/"/>'
      response['code'] = '301 Moved Permanently'
      response['type'] = 'text/html'
  else:
    logger.error('Invalid request method.')
    response['content'] = usage
    response['code'] = '405 Method Not Allowed'
    response['type'] = 'text/html'

  start_response(response['code'], [
    ("Content-Type", response['type']),
    ("Content-Length", str(len(response['content'])))
  ])
  return [bytes(response['content'], 'utf-8')]
