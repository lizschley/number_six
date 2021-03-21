'''
    this is a one time cleanup, may reuse later

    Takes normal json created by scripts.db_updater_s1 and makes methodical updates to each record
    It outputs the file to the normal input file for scripts.db_updater_s3 to make the db updates

    * it just takes the first json file it finds.  It doesn't check anything other than the JSON ext
    * uses ParagraphDictionaries.text_only_paragraph_updates(guid, pk_id, text) for each record
'''
import sys
import constants.common as constants
import constants.scripts as scripts
import constants.file_paths as file_paths
from helpers.no_import_common_class.paragraph_dictionaries import ParagraphDictionaries
import utilities.json_methods as json_helper
import utilities.random_methods as utils

CATERPILLARS = ('(Cat. Sci Name', '(Cat. Comm Name')

REPLACE_DICTIONARY = {
    '</p></p>': '</p>',
    '(Cat. Sci Name': 'Scientific Name',
    '(Cat. Comm Name': 'Common Name',
    '<li>': '<li class=\"plant_descriptions\">'
}


def run_edit_process():
    ''' Drives updates to the paragraphs with the mistakes and new ideas left by plant screen scraping'''
    file_path = utils.file_path_with_extension(file_paths.INPUT_DIR, constants.JSON_EXT)
    if file_path is None:
        sys.exit(f'No files with extension=={constants.JSON_EXT} in directory: {file_paths.INPUT_DIR}')
    input_data = json_helper.json_to_dict(file_path)
    output_data = loop_through_input_data(input_data)
    params = {'out_json_path': scripts.INPUT_TO_UPDATER_STEP_THREE}
    json_helper.write_dictionary_to_file(output_data, **params)


def loop_through_input_data(input_data):
    ''' takes a dictionary as input, transforms it and returns a new dictionary '''
    output_data = {'paragraphs': []}
    for para in input_data['paragraphs']:
        new_text = edit_para_text(para['text'])
        new_para = ParagraphDictionaries.text_only_paragraph_updates(para['guid'],
                                                                     para['id'],
                                                                     new_text)
        output_data['paragraphs'].append(new_para)
    return output_data


def edit_para_text(text):
    ''' fix all the little problems in the text '''
    if add_end_para_tag(text):
        text = text + '</p>'
    new_text = replace_text(text)
    return new_text


def add_end_para_tag(text):
    ''' this may not affect the output, but end_tags make it cleaner.  '''
    last_4 = text[-4:]
    if last_4 == '</p>':
        return False
    return True


def replace_text(text):
    ''' replace the text in the REPLACE DICTIONARY.  Also delete the end paren for the caterpillars '''
    positions = []
    for key in REPLACE_DICTIONARY:
        if key in CATERPILLARS:
            positions.append(text.find(key))
        text = text.replace(key, REPLACE_DICTIONARY[key])
    if len(positions) == 0:
        return text
    for start_pos in positions:
        pos = text.find(')', start_pos)
        if pos == -1:
            continue
        text = text[:pos] + text[pos + 1:]
    return text
