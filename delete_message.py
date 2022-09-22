#import json
from botocore.exceptions import ClientError

def delete_message(sqs_client, message, queue):
    try:
        response = sqs_client.delete_message(
            QueueUrl=queue,
            ReceiptHandle=message['Messages'][0]['ReceiptHandle']
        )
        print("message deleted")
    except ClientError:
        print("couldn't delete messages from the queue")
    else:
        return response

def delete_multiple_messages(sqs_client, messages, queue):
 #   print("message starts: ", json.dumps(messages, indent=4))
    try:
        response = sqs_client.delete_message_batch(
            QueueUrl=queue,
            Entries=[
                {
                    'Id': messages['MessageId'],
                    'ReceiptHandle': messages['ReceiptHandle']
                },
            ]
        )
        print("messages deleted")
    except ClientError:
        print("couldn't delete messages from the queue")
    else:
        return response
