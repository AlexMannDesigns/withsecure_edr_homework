#import json
from botocore.exceptions import ClientError

def delete_message(sqs_client, message, queue):
    try:
        response = sqs_client.delete_message(
            QueueUrl=queue,
            ReceiptHandle=message['Messages'][0]['ReceiptHandle']
        )
    except ClientError:
        print("couldn't delete messages from the queue")
    else:
        return response

def create_entry(message):
    Id = message['MessageId']
    ReceiptHandle = message['ReceiptHandle']
    value = {
        'Id': Id, 
        'ReceiptHandle': ReceiptHandle
    }
    return value

def delete_multiple_messages(sqs_client, messages, queue):
    entries = []
    for message in messages['Messages']:
        entry = create_entry(message)
        entries.append(entry)
    try:
        response = sqs_client.delete_message_batch(
            QueueUrl=queue,
            Entries=entries
        )
    except ClientError:
        print("couldn't delete messages from the queue")
    else:
        return response
