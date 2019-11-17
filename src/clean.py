
def set_key(dictionary, key, value):
    '''
    Function that fills dictionaries.
    Create keys if they do not yet exist and/or add values to existing keys.
    '''
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]





