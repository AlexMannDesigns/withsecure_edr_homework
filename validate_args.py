import sys
from try_parse_int import *

# messages read and visibility timeout must be configurable, so these can be read from cmd line
# We want to be sure that args 1 & 2 are both numeric values within the appropriate ranges
# if the args are invalid, or just not included, then we can display a usage message

def validate_args():
    if (len(sys.argv) != 3
    or not try_parse_int(sys.argv[1])
    or not try_parse_int(sys.argv[2])
    or not int(sys.argv[1]) in range(1, 11)
    or not int(sys.argv[2]) in range(0, 43201)):
        print("""Usage: python3 main.py arg1 arg2
        arg1 = the number of messages to read from the queue (min = 1, max = 10)
        arg2 = the duration (in seconds) those messages are visible after being received (min = 0, max = 43200)
        NB: both args must be numeric values""")
        return False
    return True
