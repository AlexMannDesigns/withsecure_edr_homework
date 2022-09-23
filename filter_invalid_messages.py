import json
import base64

# events published to the output stream must have:
#   - an event type (new_process or network_connection)
#   - a unique identifier (submission_id)
#   - a source device identifier (device_id)
#   - a time stamp (time_created)

# The first part of the process is to check that data has the above keys included
# The second part of the process is to check the values of those keys, to ensure
# they are valid.
# In the case of the device_id and submission_id, the string's follow the following format:
#       XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX (X = alphanumeric char)
# We can therefore ensure these are valid by checking the length, then checking each section
# delimited by '-' chars contains only alphanumeric characters, and '-' chars are at the correct
# inidicies of the string
# We can also validate the time string through a similar process, but I ran out of time to do this
# so in this implementation, we are only checking the length, which should be uniform.
# A more rigorous validation process for the 'events', as I notice we have a user called 'evil-guy',
# who it would probably be sensible to keep track of. Unfortunately I ran out of time to implement this
# so, for now, we can just check the length of the data to ensure there is something there.
# When invalid data is found, we use del to remove the current item from the batch of messages.

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

def validate_values(obj):
    dev = obj['device_id']
    sub = obj['submission_id']
    time = obj['time_created']

    if len(sub) != 36 or len(dev) != 36 or len(time) != 26:
        return False
    if (not sub[0:8].isalnum() or not dev[0:8].isalnum()
        or not sub[9:13].isalnum() or not dev[9:13].isalnum()
        or not sub[14:18].isalnum() or not dev[14:18].isalnum()
        or not sub[19:23].isalnum() or not dev[19:23].isalnum()
        or not sub[24:36].isalnum() or not dev[24:36].isalnum()
        or not sub[8] == '-' or not dev[8] == '-'
        or not sub[13] == '-' or not dev [13] == '-'
        or not sub[18] == '-' or not dev[18] == '-'
        or not sub[23] == '-' or not dev[23] == '-'):
        return False
    if 'new_process' in obj['events']:
        if len(obj['events']['new_process']) == 0:
            return False
    if 'network_connection' in obj['events']:
        if len(obj['events']['network_connection']) == 0:
            return False
    return True

def check_message(obj):
    if validate_keys(obj) == False:
        return False
    if validate_values(obj) == False:
        return False
    return True

def filter_invalid_messages(messages):
    i = 0
    for message in messages['Messages']:    
        json_obj = decode_to_json(message)
        if check_message(json_obj) == False:
            del messages['Messages'][i]
        i += 1
