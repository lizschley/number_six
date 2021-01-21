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

    :param str_to_split: can be any string, but currently the snake_cased input keys from the JSON input
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


def initiate_paragraph_associations(para, key_vars, association_list=None):
    '''
    add_ref_para_associations is a convenience method allowing the user to simply list the link text
    associated with given para, instead of having to manually associate each link to its paragraph

    for example, we may create and assign an association list as follows:
    self.input_data["add_paragraph_reference"] = [{"paragraph_guid": "val", "reference_slug": "val"}]

    :param para: one para
    :type para: dict
    :param key_vars: key to a foreign key's identifier field name or its value
    :type key_vars: dictionary of strings
    :param association_list: existing association records, works with None (default)
    :type association_list: list, optional
    :return: the dicionary with the keys and values necessary to create paragraph reference associations
    :rtype: dict
    '''
    if key_not_in_dictionary(para, key_vars['para_val_2_key']):
        return
    if not para[key_vars['para_val_2_key']]:
        return

    return add_to_associations(key_vars['key_1'],
                               para[key_vars['para_val_1_key']],
                               key_vars['key_2'],
                               para[key_vars['para_val_2_key']],
                               association_list)


def add_to_associations(key_1, val_1, key_2, val_2_list, association_list):
    '''
    add_to_associations makes creating content easier.  Rather than creating the many
    to many JSON input, simply add a list of values that are associated with a given key.

    To make more generic: pass in all of the key and values and also the return record
    list, though if there is no return list, we simply pass back a new list of association records.

    This does not any extra fields associated with the association itself.

    :param Key_1: foreign key name
    :type Key_1: str
    :param val_1: foreign key value that is the same for all of the association records created
    :type val_1: same as the input value (most likely str)
    :param key_2: foreign key name
    :type key_2: str
    :param val_2_list: list of values, each one on the list will make a new association record
    :type val_2_list: list
    :param association_list: list of existing association records, defaults to None
    :type association_list: list, optional
    :return: list of association records.  There may be some existing, but there is probably some that
             are added
    :rtype: list
    '''
    association_list = [] if association_list is None else association_list
    for val_2 in val_2_list:
        new_association = {}
        new_association[key_1] = val_1
        new_association[key_2] = val_2
        association_list.append(new_association)
    return association_list


def pop_keys(keys_to_pop, dict_to_check):
    '''
    pop_keys gets rid of unwanted keys

    :param keys_to_pop: list of keys that we don't want
    :type keys_to_pop: list of strings
    :param dict_with_keys: dictionary that might have extraneous keys
    :type dict_with_keys: dict
    '''
    for key in keys_to_pop:
        if key_in_dictionary(dict_to_check, key):
            dict_to_check.pop(key)
    return dict_to_check


def no_keys_from_list_in_dictionary(key_list, dict_to_check):
    '''
    no_keys_from_list_in_dictionary returns True if any of the keys in the key list
    is in the dictionary

    Otherwise return False

    :param key_list: list of keys
    :type key_list: list of strings
    :param dict_to_check: dictionary to check for keys in list
    :type dict_to_check: dict
    :return: False if any of the keys from the list are in the dictionary, else True
    :rtype: bool
    '''
    keys = dict_to_check.keys()
    for key in keys:
        if key in key_list:
            return False
    return True
