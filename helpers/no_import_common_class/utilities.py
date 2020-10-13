''' Useful within programs and classes '''


def find_dictionary_from_list_by_key_and_value(dictionary_list, key, value):
    '''
    find_dictionary_from_list_by_key_and_value given a list of dictionaries, and a key/value pair,
    will find any dictionaries with the given key and value.

    Works without KeyError if one of the dictionaries in the list does not have the key

    :param dictionary_list: list of dictionaries
    :type dictionary_list: list
    :param field: name of field in name/value pair
    :type field: string
    :param value: value of field in name/value pair
    :type value: variable, but most likely a string
    :return: results from search -> list of dictionaries
    :rtype: list
    '''
    copy_list = dictionary_list.copy()
    for idx, dictionary in enumerate(copy_list):
        if key_not_in_dictionary(dictionary, key):
            copy_list.pop(idx)
    return list(filter(lambda dict_in: dict_in[key] == value, copy_list))


def find_value_from_dictionary_list(dictionary_list, key):
    '''
    find_value_from_dictionary_list find value, when you don't know which dictionary has key

    :param dictionary_list: list of dictionaries
    :type dictionary_list: list
    :param key: name of key in key/value pair
    :type key: string
    :return: results from search -> list of whatever type the value is
    :rtype: list
    '''
    return [d[key] for d in dictionary_list if key in d]


def key_not_in_dictionary(dict_to_check, key):
    '''
    key_not_in_dictionary returns true if key not in dictionary, else false

    :param dict_to_check: pass in the dictionary in question
    :type dict_to_check: dictionary
    :param key: key we are looking for
    :type key: depends on input
    :return: True if key is in dict_to_check else false
    :rtype: bool
    '''
    default = 'hopefully$$** never___ TO return~~~%^&'
    val = dict_to_check.get(key, default)
    return val == default


def key_in_dictionary(dict_to_check, key):
    '''
    key_in_dictionary returns true if key in dictionary, else false

    :param dict_to_check: pass in the dictionary in question
    :type dict_to_check: dictionary
    :param key: key we are looking for
    :type key: string
    :return: False if key not in dict_to_check else True
    :rtype: bool
    '''
    default = 'hopefully$$** never___ TO return~~~%^&'
    val = dict_to_check.get(key, default)
    return val != default


def dictionary_key_begins_with_substring(search_dict, subs):
    '''
    dictionary_keys_begins_with_substring returns true if any key starts with substring
    otherwise returns false

    :param search_list: list to be searched
    :type search_list: list of strings
    :param subs: substring to search for
    :type subs: string
    '''

    return bool([idx for idx in search_dict if idx.lower().startswith(subs.lower())])


def dict_from_split_string(str_to_split, split_var, field_names):
    '''
    dict_from_split_string is an aid to make processing generic.  The update paragraphs process, parses
    the input data keys in order to know what constants to use to find the necessary information.

    Based on the returning dictionary, the program will call the correct generic methods, with the
    correct arguments.

    :param str_to_split: can be any string, but currently the camel_cased input keys from the JSON input
    :type str_to_split: str
    :param split_var: string to split on, for example: '_', but could be anything really
    :type split_var: str
    :param field_names: Tuple containing the keys of the dictionary, the string that is split supplies
    the values
    :type field_names: Tuple of strings
    :return: Dictionary with the fieldnames as keys and the pieces of the split string as values
    :rtype: dict
    '''
    return_dict = {}
    temp = str_to_split.split(split_var)
    if len(temp) < len(field_names):
        return {
            'error': ('Programming Error!  There are two many field_names for the string to split.'
                      f'string to split== {str_to_split} & field_names == {field_names}')
        }
    for idx, name in enumerate(field_names):
        return_dict[name] = temp[idx]
    return return_dict
