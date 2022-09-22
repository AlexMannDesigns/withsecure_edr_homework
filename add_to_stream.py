from botocore.exceptions import ClientError

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

