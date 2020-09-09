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
    :type key: string
    :return: True if key is in dict_to_check else false
    :rtype: bool
    '''
    return dict_to_check.get(key, 'ab2b-8bf1f660ae48') == 'ab2b-8bf1f660ae48'


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
    return not dict_to_check.get(key, 'ab2b-8bf1f660ae48') == 'ab2b-8bf1f660ae48'


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
