from botocore.exceptions import ClientError

# Similar to delete_message, here we want to be able to send data to the output
# stream in batches. I have used the same process here to allow this to happen,
# by adding a helper function to build a list, then passing that list as a param
# in the put_records function call.
# The return value of put_records is returned to main for ease of debugging

def create_record(message):
    data = message['Body']
    partition_key = message['MD5OfBody']

    value = {
        'Data': data,
        'PartitionKey': partition_key
    }
    return value
            

def add_to_stream(kinesis_client, stream_name, messages):
    records = []
    for message in messages['Messages']:
        record = create_record(message)
        records.append(record)
    try:
        response = kinesis_client.put_records(
        Records=records,
        StreamName=stream_name 
    )
    except ClientError as error:
        print("Couldn't add data to stream")
    else:
         return response

