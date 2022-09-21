import boto3
import base64
import json

"""program setup"""

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

response = client.receive_message(QueueUrl='http://localstack:4566/000000000000/submissions')

"""decoding to json"""

code = response['Messages'][0]['Body']
decoded_bytes = base64.standard_b64decode(code)
decoded_str = decoded_bytes.decode("ascii")
json_str=json.loads(decoded_str)

"""debug print for testing"""
print(json.dumps(json_str['events'], indent=4))
