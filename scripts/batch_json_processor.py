'''
    [summary]

[extended_summary]

:return: [description]
:rtype: [type]
'''
import os
from pprint import pprint
from portfolio.settings import BASE_DIR
import helpers.import_common_class.paragraph_helpers as ph

JSON_DATA_ROOT = os.path.join(BASE_DIR, 'data')
SCRIPT_PARAM_SUBSTR = {'filename': '.json', 'process': 'process=',
                       'test_run': 'test_run:', }
DB_UPDATE = 'db_update'
OK_PROCESSES = ['para_display', 'para_to_db', ]


def run(*args):
    '''
        usage as follows:
        > python manage.py runscript -v3  batch_json_processor --script-args
                /Users/liz/development/number_six/test/test.json
        or > python manage.py runscript -v3  batch_json_processor
    '''
    filename = filename_checker(args, SCRIPT_PARAM_SUBSTR['filename'])
    print(f'filename == {filename}')

    process = process_checker(args, SCRIPT_PARAM_SUBSTR['process'])
    if process == DB_UPDATE:
        print('Running the db update process.')
        ph.paragraph_json_to_db(filename)
    else:
        paragraphs = ph.paragraph_list_from_json(filename)
        pprint(paragraphs)


def filename_checker(args, subs):
    '''
    filename_checker [summary]

    [extended_summary]

    :param args: [description]
    :type args: [type]
    :param subs: [description]
    :type subs: [type]
    :return: [description]
    :rtype: [type]
    '''
    filenames = check_for_args(args, subs)
    if len(filenames) > 1:
        # if passing > 1 argument that passes extension test
        print('Have not implemented passing in > one specific filename and path.')
        exit(0)
    elif len(filenames) < 1:
        # if no arguments, get first filename that passes extension test in correct directory
        # could do in a loop, but extra work unless reason presents itself
        print('Taking first file with a json extension from the default data directory')
        filenames = check_for_args(os.listdir(JSON_DATA_ROOT), subs)
        if len(filenames) < 1:
            print('No json files in default directory and no json file as input parameter')
            exit(0)
        return os.path.join(JSON_DATA_ROOT, filenames[0])
    else:
        print(f'Using json file passed in as a parameter: {filenames[0]}')
        return filenames[0]


def process_checker(args, subs):
    possibilities = check_for_args(args, subs)
    if len(possibilities) != 1:
        return []
    possibility = possibilities[0]
    process_array = possibility.split('=')
    return process_array[1] if len(process_array) == 2 else []


def check_for_args(args, subs):
    return [i for i in args if subs in i]
