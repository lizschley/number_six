''' Methods that are not specific to Paragraph functionality, but could be useful '''
import os
import shutil
import sys
from decouple import config
from django.utils.text import slugify
import constants.scripts as scripts


def valid_non_blank_string(str_to_check):
    '''
    valid_non_blank_string returns True if str_to_check is a valid string with more than just whitespace

    :param str_to_check: string to check
    :type str_to_check: str
    :return: True if it is a valid string that contains more than whitespace, else False
    :rtype: bool
    '''
    if not str_to_check:
        return False
    try:
        res = str_to_check.isspace()
    except AttributeError:
        return False
    return not res


def slugify_string(input_str):
    '''
    slugify_string slugifies the input string.  This is a convenience method, currently for creating
    reference links for a new reference record in a new paragraph record.

    :param input_str: string to slugify
    :type input_str: str
    :return: slugified version of the input string
    :rtype: str
    '''
    return slugify(input_str)


def archive_files_from_input_directories(include_not_done=True):
    '''
    archive_files_from_input_directories moves the files used for processing input data to
    the archive location

    :param include_done: whether to also move files that haven't been manually moved to done or loaded
    :type include_done: bool, optional
    '''
    in_dirs = scripts.ONLY_DONE_INPUT_DIRECTORIES
    num_processed = 0
    if include_not_done:
        in_dirs += scripts.NOT_DONE_INPUT_DIRECTORIES
    num_processed = 0
    target = config('USED_INPUT_FINAL_DIRECTORY', default='')
    if len(target) < 10:
        sys.exit('Target directory does not exist. Checks USED_INPUT_FINAL_DIRECTORY env variable')
    for dir_path in in_dirs:
        params = {'in_dir': dir_path,
                  'out_dir': target,
                  'check_extension': True,
                  'extensions': ['.json'],
                  'num_processed': num_processed}
        num_processed = loop_through_files_to_move(**params)
    print(f'After looping through the input data, {num_processed} files were moved.')


def loop_through_files_to_move(**kwargs):
    '''
    loop_through_files_to_move moves all the files from input directory to output directory

    :param input_dir_path: directory containing files to loop through, this is a shallow loop.
    :type input_dir_path: str
    :return: number of files that were moved
    :rtype: int
    '''
    input_dir_path = kwargs.get('in_dir')
    output_dir_path = kwargs.get('out_dir')
    check_extension = kwargs.get('check_extension', False)
    extensions = kwargs.get('extensions')
    num_processed = kwargs.get('num_processed', 0)
    for filename in os.listdir(input_dir_path):
        if check_extension and filename not in extensions:
            continue
        output_path = os.path.join(output_dir_path, filename)
        input_path = os.path.join(input_dir_path, filename)
        shutil.move(input_path, output_path)
        num_processed += 1
    return num_processed


def copy_file_from_source_to_target(source, target):
    '''
    copy_file_from_source_to_target to target.  Both source and target should have
    a complete file_path

    :param source: path to source file path
    :param target: path to target file path
    '''

    try:
        shutil.copyfile(source, target)
    except IOError as err:
        print(f'Unable to copy file from {source} to {target}')
        sys.exit(f'Error: {err}')


def replace_line(**kwargs):
    ''' replace_line replaces one line in the base.html file '''
    with open(kwargs['in_file']) as fin, open(kwargs['out_file'], 'w') as fout:
        for line in fin:
            lineout = line
            if kwargs['sub_str'] in line:
                lineout = f'{kwargs["new_line"]}\n'
            fout.write(lineout)


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
