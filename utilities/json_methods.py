''' This is a json utility method.  It only has json extracted from business logic '''
from datetime import datetime
import json
import constants.scripts as constants
import utilities.date_time as dt


def write_json_file(path_to_json, output_data):
    '''
    write_json_file writes the formatted file necessary to update the paragraph
    structure in the db
    This test mainly for testing
    '''
    with open(path_to_json, 'w') as file_path:
        json.dump(output_data, file_path)


def json_to_dict(json_path):
    '''
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


def update_json_file(updated_json_object, file_path):
    '''
    update_json_file takes the file path and updated json object and writes the json
    with the new updates

    :param updated_json_object: this will be updated as part of another process
    :type updated_json_object: dictionary
    :param file_path: This is the path to the json file
    :type file_path: str
    '''
    file_to_update = open(file_path, 'w')
    json.dump(updated_json_object, file_to_update)
    file_to_update.close()


def write_dictionary_to_file(output_data, **kwargs):
    '''
    write_dictionary_to_file is a method that can be used generically, though there are some defaults

    Key word args are optional:
    prefix will be input_, unless you override
    filename will be prefix_datetime.json unless you override (note = won't use prefix if you provide
                filename)
    directory_path will be base path + data/data_for_creates unless you override

    :param input_data: dictionary to be written to json
    :type input_data: dictionary
    '''
    output_file = open(create_json_file_path(**kwargs), 'w')
    # magic happens here to make it pretty-printed
    output_file.write(json.dumps(output_data, default=dt.postgres_friendly_datetime,
                                 indent=4, sort_keys=True))
    output_file.close()


def create_json_file_path(**kwargs):
    '''
    create_json_file_name_with_path creates json output file

    :param directory_path: directory to write to.  defaults to OUT_JSON_PATH, which is always wrong
    :type directory_path: str, optional
    :param filename: if filename is None will create filename with datetime stamp, defaults to None
    :type filename: str, optional
    :return: file_path
    :rtype: str
    '''
    prefix = kwargs.get('prefix', constants.DEFAULT_PREFIX)
    out_json_path = kwargs.get('out_json_path', constants.INPUT_CREATE_JSON)
    filename = kwargs.get('filename',
                          prefix + datetime.now().isoformat(timespec='seconds') + '.json')
    directory_path = kwargs.get('directory_path', out_json_path)

    if filename is None:
        filename = prefix + datetime.now().isoformat(timespec='seconds') + '.json'

    return directory_path + '/' + filename
