'''
    this is a one time cleanup, may reuse later

    Takes normal json created by scripts.db_updater_s1 and makes methodical updates to each record
    It outputs the file to the normal input file for scripts.db_updater_s3 to make the db updates

    * it just takes the first json file it finds.  It doesn't check anything other than the JSON ext
    * uses ParagraphDictionaries.text_only_paragraph_updates(guid, pk_id, text) for each record
'''
import sys
import constants.common as constants
import constants.file_paths as file_paths
import utilities.json_methods as json_helper
import utilities.random_methods as utils
import utilities.debug as me


def run_analysis():
    ''' Drives updates to the paragraphs with the mistakes and new ideas left by plant screen scraping'''
    file_path = utils.file_path_with_extension(file_paths.INPUT_DIR, constants.JSON_EXT)
    if file_path is None:
        sys.exit(f'No files with extension=={constants.JSON_EXT} in directory: {file_paths.INPUT_DIR}')
    input_data = json_helper.json_to_dict(file_path)
    loop_through_paras(input_data)
    loop_through_gp(input_data)


def loop_through_paras(indata):
    ''' takes a dictionary as input, transforms it and returns a new dictionary '''
    print(f'num paras =={len(indata["paragraphs"])}')
    print(f'num gp =={len(indata["group_paragraph"])}')
    no_guid = 0
    no_id = 0
    for para in indata['paragraphs']:
        guid = para['guid']
        pk_id = para['id']
        subtitle = para['subtitle']
        str_id = str(pk_id)
        if utils.key_not_in_dictionary(indata['record_lookups']['paragraphs'], guid):
            no_guid += 1

            print(f'{no_guid}. no guid key for subtitle=={subtitle}')
        if utils.key_not_in_dictionary(indata['record_lookups']['paragraphs'], str_id):
            no_id += 1
            print(f'{no_id}. no pk_id key for subtitle=={subtitle}')
        else:
            print(f'results for subtitle=={subtitle}:')
            res = utils.find_dictionary_from_list_by_key_and_value(indata['group_paragraph'],
                                                                   'paragraph_id',
                                                                   pk_id)
            print(f'group_para = {res}')


def loop_through_gp(indata):
    ''' takes a dictionary as input, transforms it and returns a new dictionary '''
    for gp in indata['group_paragraph']:
        para_id = gp['paragraph_id']
        res = utils.find_dictionary_from_list_by_key_and_value(indata['paragraphs'], 'id', para_id)
        print(f'got para with subtitle == {res[0]["subtitle"]}')