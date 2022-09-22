# Todo
# read from queue in a loop - DONE
# create validation process, drop invalid data
#   - must have a unique id ('submission_id')
#   - must have a 'device_id'
#   - must have a timestamp 'time_created'
# events must be ordered in the context of a single submission
# publish validated events to the kinesis stream - DONE (validation still a wip)
# number of messages read from SQS in a single request must be configurable - DONE
# visibility timeout of those messages must be configurable - DONE

import json

import boto3
import sys
from botocore.exceptions import ClientError

from print_message_body import *
from try_parse_uint import *
from delete_message import delete_multiple_messages
from receive_message import receive_multiple_messages
from add_to_stream import add_to_stream

# Program setup
# Session must be provided with dummy credentials in order to interface with AWS
# Default endpoint url overwritten with url of localstack

session = boto3.session.Session()
sqs_client = session.client(
    'sqs',
    region_name='eu-west-1',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='ACCESS_KEY',
    aws_secret_access_key='SECRET_KEY',
    aws_session_token='SESSION_TOKEN'
)
kinesis_client = session.client(
    'kinesis',
    region_name='eu-west-1',
    endpoint_url='http://localhost:4566',
    aws_access_key_id='ACCESS_KEY',
    aws_secret_access_key='SECRET_KEY',
    aws_session_token='SESSION_TOKEN'
)

# messages read and visibility timeout must be configurable, so these can be read from cmd line
# if the args are invalid, then we can display a usage message
if (len(sys.argv) != 3
    or not try_parse_uint(sys.argv[1])
    or not try_parse_uint(sys.argv[2])
    or int(sys.argv[1]) < 1
    or int(sys.argv[1]) > 10
    or int(sys.argv[2]) < 0
    or int(sys.argv[2]) > 43200):
    print("""Usage: python3 main.py arg1 arg2
    arg1 = the number of messages to read from the queue (min = 1, max = 10)
    arg2 = the duration (in seconds) those messages are visible after being received (min = 0, max = 43200)
    NB: both args must be numeric values""")
    sys.exit()

# Variables needed for main loop
num_of_messages = int(sys.argv[1])
visibility_timeout = int(sys.argv[2])
queue = "http://localstack:4566/000000000000/submissions"
more_messages = True 

# Establishing name of output stream
# The stream we only need one stream, so the limit param is used 
# for extra safety, if we have more streams present we return an error and close the program
kinesis_response = kinesis_client.list_streams(Limit=1)

if kinesis_response['HasMoreStreams'] == True:
    print("error: check kinesis streams")
    quit()

stream_name = kinesis_response['StreamNames'][0]

'''
Validation:
    check submission_id
    check device_id
    check time_created
    check events contains a new_process or a network_connection
'''
# Idea - create a new array, check 'Messages' for errors
# Any item that passes the checking can be appended to the new array
# the 'Messages' array in the original object is replaced with the new one

def filter_invalid_messages(messages):
    print(json.dumps(messages, indent=4)) 
    res = []
    for message in messages['Messages']:
        code = message['Body']
        decoded_bytes = base64.standard_b64decode(code)
        decoded_str = decoded_bytes.decode("ascii")
        json_obj=json.loads(decoded_str)
    
        if (json_obj['submission_id'] == "not-an-uuid"
            or len(json_obj['submission_id']) != 36
            or json_obj['device_id'] == "not-an-uuid"
            or len(json_obj['device_id']) != 36
            or len(json_obj['time_created']) != 26):
                print('hello')
    return res

# control loop - the main process of the program is handled here
# The program will continuously pull messages from the queue until there is nothing left to read
# In each iteration the batch of messages is validated, outputted to the stream and then deleted

while more_messages:
    received_messages = receive_multiple_messages(sqs_client, queue, num_of_messages, visibility_timeout)
    if received_messages and 'Messages' in received_messages:
        filter_invalid_messages(received_messages)
        add_to_stream(kinesis_client, stream_name, received_messages)
        delete_multiple_messages(sqs_client, received_messages, queue)
    else:
        print(json.dumps(received_messages, indent=4))
        more_messages = False
print("done")
