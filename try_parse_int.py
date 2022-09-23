# a simple for function for confirming whether data 's' can be successfully converted to an integer
# I tried to make this as 'Pythonic' as possible by using try-except logic

def try_parse_int(s):
    try:
        x = int(s, 10)
        return True
    except ValueError:
        return False
