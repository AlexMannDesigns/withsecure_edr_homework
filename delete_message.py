from botocore.exceptions import ClientError

# As the user is able to read from the queue in batches, we need to delete
# messages in batches as well. The method implemented here is to create
# an list of objects using a helper function, so that this can be passed to
# the delete_message_batch function as the 'Entries' parameter.
# In the event of an error, a message will be printed

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
