# This function fills in default values for an options dictionary that is missing some fields
def merge_defaults(input_dict, defaults_dict):
    """
    Recursively merges default values into the input dictionary.
    For each key in defaults_dict, if the key is missing in input_dict or
    the value is None, it sets the value from defaults_dict. This function
    works recursively for nested dictionaries.

    Parameters:
    - input_dict: The dictionary to populate with default values; can be None
    - defaults_dict: The dictionary containing default values.

    Returns:
    - A dictionary with the input values overridden by the defaults where necessary.
    """
    if input_dict == None:
        input_dict = dict()

    for key, default_value in defaults_dict.items():
        if key not in input_dict or input_dict[key] is None:
            input_dict[key] = default_value
        elif isinstance(default_value, dict) and isinstance(input_dict.get(key), dict):
            merge_defaults(input_dict[key], default_value)

    return input_dict