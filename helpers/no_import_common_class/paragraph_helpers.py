'''
    Any file within the no_import_common_class is for methods that can be
    imported safely (without circular dependencies) into the classes in
    the common class folder. '''

import json


def create_link(url, link_text):
    '''
    [Summary]
    create_link: takes the input and creates a link to be used in displaying text

    :param url: will be a url to link to
    :type url: String
    :param link_text: will be the link text in the link taht will be created
    :type link_text: String
    :return: Link that will be used as a reference to its associated paragraph
    :rtype: String
    '''
    return f'<a href="{url}" target="_blank">{link_text}</a>'


def json_to_dict(json_path):
    '''
    [Summary]
    json_to_dict takes a json file path, reads the content and uses it to create a dictionary.

    :param json_path: Path to a file on the project directory structure
    :type json_path: String
    :return: dictionary based on the contents of the JSON file
    :rtype: dictionary
    '''
    # Opening JSON file
    file = open(json_path, 'r')
    # load and return JSON object as a dictionary
    data = json.load(file)
    file.close()
    return data


def format_json_text(text):
    '''
    [Summary]
     format_json_text takes a List of strings and concatenates them
       together with a space

    [extended_summary]
    If there is no html tag (just checks for < in the first character),
       it adds a paragraph tag

    :param text: List of strings
    :type text: List
    :return: html formated text
    :rtype: str
    '''
    text = ' '.join(text)
    if text[0] != '<':
        text = '<p>' + text + '</p>'
    return text


def extract_data_from_form(classification):
    '''
    [Summary]
    extract_data_from_form formats the Study lookup form return to be usable for
    queries

    [extended_summary]
    This takes data that is sent directly from the Study lookup form and
    transforms it in a way that can be used for view paramaters.  This is so the
    correct queries can be performed in the view.

    :param classification: string that has the fieldname and the value separated
        by an underscore
    :type classification: str
    :return: dictionary with key and value parsed from the input data
    :rtype: dictionary
    '''
    temp = classification.split('_')
    if len(temp) != 2:
        return {}
    try:
        return {temp[0]: int(temp[1])}
    except ValueError:
        return {}
