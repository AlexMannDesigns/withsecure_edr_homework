import sys
from try_parse_int import *

# messages read and visibility timeout must be configurable, so these can be read from cmd line
# We want to be sure that args 1 & 2 are both numeric values within the appropriate ranges
# if the args are invalid, or just not included, then we return false to display a usage message

def validate_args():
    if (len(sys.argv) != 3
    or not try_parse_int(sys.argv[1])
    or not try_parse_int(sys.argv[2])
    or not int(sys.argv[1]) in range(1, 11)
    or not int(sys.argv[2]) in range(0, 43201)):
        return False
    return True
