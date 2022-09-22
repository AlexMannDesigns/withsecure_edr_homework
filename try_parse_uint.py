def try_parse_uint(s):
    try:
        x = int(s, 10)
        return True
    except ValueError:
        return False
