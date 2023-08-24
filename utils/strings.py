def is_positive_number(value):
    try:
        num = float(value)
    except ValueError:
        return False
    return num > 0
