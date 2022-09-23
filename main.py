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
from botocore.exceptions import ClientError

import boto3
import sys

from validate_args import validate_args 
from print_message_body import *
from delete_message import delete_multiple_messages
from receive_message import receive_multiple_messages
from filter_invalid_messages import filter_invalid_messages
from add_to_stream import add_to_stream

# Setting up AWS:
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

# Establishing name of output stream:
# We only need one stream, so the limit param is used 
# For extra safety, if we have more streams present we return an error and close the program
kinesis_response = kinesis_client.list_streams(Limit=1)
if kinesis_response['HasMoreStreams'] == True:
    print("error: check kinesis streams")
    quit()
stream_name = kinesis_response['StreamNames'][0]

# The url of the queue can be hard-coded for the purposes of this project
queue = "http://localstack:4566/000000000000/submissions"

# Variables needed for main loop:
# First we check that the messages read and visibility timeout have been configured correctly
if validate_args() == False:
    quit()
num_of_messages = int(sys.argv[1])
visibility_timeout = int(sys.argv[2])

# control loop - the main process of the program is handled here
# The program will continuously pull messages from the queue until there is nothing left to read
# In each iteration the batch of messages is validated, outputted to the stream and then deleted
more_messages = True 
while more_messages:
    received_messages = receive_multiple_messages(sqs_client, queue, num_of_messages, visibility_timeout)
    if received_messages and 'Messages' in received_messages:
        filter_invalid_messages(received_messages)
        add_to_stream(kinesis_client, stream_name, received_messages)
        delete_multiple_messages(sqs_client, received_messages, queue)
        more_messages = False
    else:
        print(json.dumps(received_messages, indent=4))
        more_messages = False
print("done")
