def try_parse_uint(s):
    try:
        x = int(s, 10)
        if x > 0:
            return True
    except ValueError:
        return False
