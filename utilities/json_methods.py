''' This is a json utility method.  It only has json extracted from business logic '''
import json


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
