'''
    Any file within the no_import_common_class is for methods that can be
    imported safely (without circular dependencies) into the classes in
    the common class folder. '''

import json


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
    return f'<a href="{url}" target="_blank">{link_text}</a>'


def json_to_dict(json_path):
    '''
    This takes a json file path, reads the content and uses it to create a dictionary.

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
    text = ' '.join(text)
    if text[0] != '<':
        text = '<p>' + text + '</p>'
    return text


def ensure_unique_slug(sender, instance, slug):
    new_slug = slug
    while True:
        if not_unique(sender, new_slug):
            new_slug = f'{slug}-{instance.id}'
        else:
            break
    return new_slug


def not_unique(sender, slug):
    return sender.objects.filter(slug=slug).exists()


def extract_data_from_form(classification):
    temp = classification.split('_')
    if len(temp) != 2:
        return {}
    try:
        return {temp[0]: int(temp[1])}
    except ValueError:
        return {}
