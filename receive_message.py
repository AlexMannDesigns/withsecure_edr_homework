from botocore.exceptions import ClientError
from print_message_body import *

def receive_next_message(sqs_client, queue):
    try:
        message = sqs_client.receive_message(
                QueueUrl=queue,
        )
    except ClientError as error:
        print("Couldn't receive messages from the queue")
        raise error
    else:
        return message

def receive_multiple_messages(sqs_client, queue, num_of_messages, visibility_timeout):
    try:
        messages = sqs_client.receive_message(
                QueueUrl=queue,
                MaxNumberOfMessages=num_of_messages,
                VisibilityTimeout=visibility_timeout
        )
    except ClientError as error:
        print("Couldn't receive messages from the queue")
        raise error
    else:
        return messages
