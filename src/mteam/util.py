def bytes_to_gb(bytes, unit='b'):
    if unit.lower() == 'b':
        gb = bytes / (1024**3) 
    elif unit.lower() == 'kb':
        gb = bytes / (1024**2)  
    elif unit.lower() == 'mb':
        gb = bytes / 1024  
    else:
        raise ValueError("Invalid unit. Please use 'b', 'kb', or 'mb'.")

    return gb

def is_legal(data, limit) -> bool:
    return data in limit

def mode_legal(data, limit):
    mode_list = data.split(',')
    for mode in mode_list:
        if mode not in limit:
            if mode == "all":
                return True, limit
            else:
                return False, None
    return True, mode_list