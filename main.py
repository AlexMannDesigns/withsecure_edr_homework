# Todo
# read from queue in a loop
# create validation process, drop invalid data
#   - must have a unique id ('submission_id')
#   - must have a 'device_id'
#   - must have a timestamp 'time_created'
# events must be ordered in the context of a single submission
# publish validated events to the kinesis stream
# number of messages read from SQS in a single request must be configurable
# visibility timeout of those messages must be configurable

import boto3
import base64
import json
import sys
from try_parse_uint import *

# messages read and visibility timeout must be configurable, so these can be read from cmd line
# if the args are invalid, then we can display a usage message
if len(sys.argv) != 3 or not try_parse_uint(sys.argv[1]) or not try_parse_uint(sys.argv[2]) or int(sys.argv[1]) > 10:
    print("""Usage: python3 main.py arg1 arg2
    arg1 = the number of messages to read from the queue (min = 1, max = 10)
    arg2 = the duration (in seconds) those messages are visible after being received (min = 1)
    NB: both args must be numeric values""")
    sys.exit()

num_of_messages = int(sys.argv[1])
visibility_timeout = int(sys.argv[2])

# Program setup
# Session must be provided with dummy credentials in order to interface with AWS
# Default endpoint url overwritten with url of localstack

session = boto3.session.Session()
client = session.client(
    'sqs',
    region_name='eu-west-1',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='ACCESS_KEY',
    aws_secret_access_key='SECRET_KEY',
    aws_session_token='SESSION_TOKEN'
)

"""reading from the queue"""

response = client.receive_message(
        QueueUrl='http://localstack:4566/000000000000/submissions',

    )

"""decoding to json"""

code = response['Messages'][0]['Body']
decoded_bytes = base64.standard_b64decode(code)
decoded_str = decoded_bytes.decode("ascii")
json_str=json.loads(decoded_str)

"""debug print for testing"""
print(json.dumps(json_str, indent=4))

