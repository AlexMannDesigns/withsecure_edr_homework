from botocore.exceptions import ClientError

# This function will retreive messages from the queue and return them back to main
# for processing, then deletion.
# The num_of_messages and visibility_timeout params are configured by the user and
# sent to the AWS api here.

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
