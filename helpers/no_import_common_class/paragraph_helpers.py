'''
    Any file within the no_import_common_class folder is for methods that can be
    imported safely (without circular dependencies) into the classes in
    the common class folder.
'''

import os
from operator import itemgetter
import constants.para_lookup as lookup
import constants.scripts as constants


def create_link(url, link_text):
    '''
    create_link: takes the input and creates a link to be used in displaying text

    :param url: will be a url to link to
    :type url: String
    :param link_text: will be the link text in the link taht will be created
    :type link_text: String
    :return: Link that will be used as a reference to its associated paragraph
    :rtype: String
    '''
    return f'<a href="{url}" class="reference_link" target="_blank">{link_text}</a>'


def add_paragraphs_to_context(context, paragraphs):
    '''
    add_paragraphs_to_context reformats data to save work in the template

    :param context: original context, minus what was needed for para retrieval
    :type context: dict
    :param paragraphs: paragraph dictionary before adding to context
    :type paragraphs: dict
    :return: context - will be used in paragraph template
    :rtype: dict
    '''
    context['title'] = paragraphs['title']
    context['title_note'] = paragraphs['title_note']
    context['paragraphs'] = paragraphs['paragraphs']
    context['ordered'] = not paragraphs['group_type'] == 'standalone'
    return context


def add_error_to_context(context, paragraphs, key):
    '''
    add_error_to_context reformats data to save work in the template

    :param context: original context, minus what was needed for para retrieval
    :type context: dict
    :param paragraphs: paragraph dictionary before adding to context
    :type paragraphs: dict
    :return: context - will be used in paragraph template
    :rtype: dict
    '''
    context['error'] = paragraphs[key]
    context['title'] = ""
    context['title_note'] = ""
    context['paragraphs'] = []
    return context


def sort_paragraphs(list_to_be_sorted, key_to_sort):
    '''
    sort_paragraphs sorts paragraphs

    :param list_to_be_sorted: paragraph list from paragraph retriever (has order field)
    :type list_to_be_sorted: sorted list of hashes
    '''
    return sorted(list_to_be_sorted, key=itemgetter(key_to_sort))


def check_for_batch_args(args, subs):
    '''
    This is for batch processing

    args is a tuple

    :param list_to_be_sorted: finds if substr is in args
    :type list_to_be_sorted: str
    '''
    return [i for i in args if subs in i]


def add_image_information(para):
    '''
    add_image_information returns the information to display an image correctly or an unchanged para

    1. Path is in format to be used by template (originally from db or json input)
    2. Alt is based on the filename
    3. Classes are based on the image_info_key (from db or json input) to image_info lookup dictionary.

    :param para: para that is originally retrieved from JSON or db
    :type para: dict
    :return: para that has image information added, if there is an image path
    :rtype: dict
    '''

    if len(para['image_path']) == 0:
        para['image_alt'] = ''
        para['image_classes'] = ''
        return para
    alt_array = os.path.splitext(para['image_path'])[0].split('/')
    para['image_alt'] = alt_array[-1]
    info = lookup.IMAGE_INFO_LOOKUP[para['image_info_key']]
    para['image_classes'] = info['classes']
    return para


def loop_through_files_for_db_updates(method, process_data):
    ''' Loops through files in directory and processes each individually '''
    directory = process_data['input_directory']
    num_processed = 0
    file_list = sorted_files_in_dir(directory, True)
    for filename in file_list:
        if use_file(filename, str(method), process_data):
            file_path = os.path.join(directory, filename)
            num_processed += 1
            process_data['file_data'] = json_to_dict(file_path)
            method(process_data)
        else:
            continue
    return num_processed


def sorted_files_in_dir(directory, descending=False):
    '''
    sorted_files_in_dir uses directory name to get list of files and sort it by filename

    :param directory: directory name and path
    :type directory: str
    :param descending: whether to sort alphebetically or in reverse, defaults to False
    :type descending: bool, optional
    :return: sorted list of files
    :rtype: list
    '''
    list_of_files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            list_of_files.append(filename)
    list_of_files.sort(reverse=descending)
    return list_of_files


def use_file(filename, method, process_data):
    '''
    use_file returns false if the extension is not json

    If it is Step One, that is enough for use_file to return True

    If Step Three, need to check if production or running as if it's production:

    if production, use_file returns True if file has production prefix or
    if not production, use_file returns True if file does not have production prefix

    Otherwise use_file returns False

    :param filename: filename (without path)
    :type filename: str
    :param method: string representation of method name (tell whether step 1 or 3)
    :type method: str
    :param process_data: passed in: environment (from environment variable) or run_as_prod, script arg
    :type process_data: dictionary
    :return: Depending on factors mentioned above, pass back True if file is correct oe False, elsewise
    :rtype: bool
    '''
    if not filename.endswith(constants.JSON_SUB):
        return False
    if 'step_three' not in method:
        return True
    if treat_like_production(process_data):
        return filename.startswith(constants.PROD_PROCESS_IND)
    return not filename.startswith(constants.PROD_PROCESS_IND)


def treat_like_production(process_data):
    '''
    treat_like_production returns true if it is the production environment (is_prod is True) or
    if we are running as prod

    :param process_data: dictionary that contains is_prod and run_as_prod information
    :type process_data: dict
    :return: whether or not we should treat it like production
    :rtype: bool
    '''
    return process_data['is_prod'] or process_data['run_as_prod']
