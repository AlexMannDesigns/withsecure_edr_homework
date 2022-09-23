import json
import base64
'''
Validation:
    check submission_id
    check device_id
    check time_created
    check events contains a new_process or a network_connection
'''
def decode_to_json(message):
    code = message['Body']
    decoded_bytes = base64.standard_b64decode(code)
    decoded_str = decoded_bytes.decode("ascii")
    return json.loads(decoded_str)

def validate_keys(obj):
    if ('submission_id' not in obj 
        or 'device_id' not in obj
        or 'time_created' not in obj
        or 'events' not in obj):
        return False
    if ('new_process' not in obj['events']
        or 'network_connection' not in obj['events']):
        return False
    return True

def check_message(obj):
    print(json.dumps(obj, indent=4))    

    if validate_keys(obj) == False:
        return False
    
    if (obj['submission_id'] == "not-an-uuid"
        or len(obj['submission_id']) != 36
        or obj['device_id'] == "not-an-uuid"
        or len(obj['device_id']) != 36
        or len(obj['time_created']) != 26):
        return False
    return True

def filter_invalid_messages(messages):
    print("original:")
    print(json.dumps(messages, indent=4)) 
    i = 0
    for message in messages['Messages']:    
        json_obj = decode_to_json(message)
        if check_message(json_obj) == False:
            del messages['Messages'][i]
        i += 1
