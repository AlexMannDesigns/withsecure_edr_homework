import json
import base64

# a simple function to help with debugging. Decodes the body from base64
# and prints to stdout in pretty format json

def print_message_body(message):
     code = message['Body']
     decoded_bytes = base64.standard_b64decode(code)
     decoded_str = decoded_bytes.decode("ascii")
     json_str=json.loads(decoded_str)
     print(json.dumps(json_str, indent=4))
