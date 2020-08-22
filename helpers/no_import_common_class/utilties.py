''' Useful within programs and classes '''


def find_dictionaries_from_value_in_list(dictionary_list, field, value):
    '''
    find_dictionaries_from_value_in_list find dict in a list of dictionaries by value of given field

    :param dictionary_list: list of dictionaries
    :type dictionary_list: list
    :param field: name of field in name/value pair
    :type field: string
    :param value: value of field in name/value pair
    :type value: variable, but most likely a string
    :return: results from search -> list of dictionaries
    :rtype: list
    '''
    return list(filter(lambda dict_in: dict_in[field] == value, dictionary_list))


def find_value_from_dictionary_list(dictionary_list, key):
    '''
    find_value_from_dictionary_list find value, when you don't know which dictionary has key

    :param dictionary_list: list of dictionaries
    :type dictionary_list: list
    :param key: name of field in name/value pair
    :type key: string
    :return: results from search -> value (probably str)
    :rtype: string?
    '''
    return [d[key] for d in dictionary_list if key in d][0]
