import json
import base64
'''
Validation:
    check submission_id
    check device_id
    check time_created
    check events contains a new_process or a network_connection
'''
# Idea - create a new array, check 'Messages' for errors
# Any item that passes the checking can be appended to the new array
# the 'Messages' array in the original object is replaced with the new one

def decode_to_json(message):
    code = message['Body']
    decoded_bytes = base64.standard_b64decode(code)
    decoded_str = decoded_bytes.decode("ascii")
    return json.loads(decoded_str)

def filter_invalid_messages(messages):
#    print(json.dumps(messages, indent=4)) 
    res = []
    for message in messages['Messages']:    
        json_obj = decode_to_json(message)
        print(json_obj['submission_id'])    
        if (json_obj['submission_id'] == "not-an-uuid"
        or len(json_obj['submission_id']) != 36
        or json_obj['device_id'] == "not-an-uuid"
        or len(json_obj['device_id']) != 36
        or len(json_obj['time_created']) != 26):
            print('hello')
    return res
