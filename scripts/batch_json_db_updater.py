'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Three part process:
    1. read data, write json to be editted
    2. edit the data manually (only what you want updated, delete the rest)
    3. do the update by reading the file.

:returns: nothing
'''
import os
from pprint import pprint
from portfolio.settings import BASE_DIR
import helpers.import_common_class.paragraph_helpers as import_helper
import helpers.no_import_common_class.paragraph_helpers as no_import_helper

JSON_DATA_ROOT = os.path.join(BASE_DIR, 'data/update_json')
VALID_ARGS_SUBS = ['date=', 'group_id=', 'guid=', 'subtitle', 'category_title',
                   'group_title', 'category_id=', 'para_id=']
VALID_ARGS = ['init_json', 'process_json', 'updating']


def run(*args):
    '''
        usage as follows:
        step 1> python manage.py runscript -v3  batch_json_db_updater --script-args init_json group_id=7
        * Note - step 2 is to update the file with your desired changes
        or
        * note - if no updating arg, will be trial_run, also need to create the file first
        step 3> python manage.py runscript -v3  batch_json_db_updater --script-args process_json
    '''
    filename = filename_checker(args, SCRIPT_PARAM_SUBSTR['filename'])
    print(f'filename == {filename}')

    process = process_checker(args, SCRIPT_PARAM_SUBSTR['process'])
    if process == DB_UPDATE:
        print('Running the db update process.')
        import_helper.paragraph_json_to_db(filename)
    else:
        paragraphs = import_helper.paragraph_list_from_json(filename)
        pprint(paragraphs)


def filename_checker(args, subs):
    '''
    filename_checker looks for filename (& path) for json file, if there are none, will check
    normal directory for the filename (& path)

    :param args: args to batch program
    :type args: dictionary
    :param subs: substr to look for (filename & path in this case)
    :type subs: str
    :return: filename & path
    :rtype: str
    '''
    print(f'args type is {type(args)}')
    filenames = no_import_helper.check_for_batch_args(args, subs)
    if len(filenames) > 1:
        # if passing > 1 argument that passes extension test
        print('Have not implemented passing in > one specific filename and path.')
        exit(0)
    elif len(filenames) < 1:
        # if no arguments, get first filename that passes extension test in correct directory
        # could do in a loop, but extra work unless reason presents itself
        print('Taking first file with a json extension from the default data directory')
        filenames = no_import_helper.check_for_batch_args(os.listdir(JSON_DATA_ROOT), subs)
        if len(filenames) < 1:
            print('No json files in default directory and no json file as input parameter')
            exit(0)
        return os.path.join(JSON_DATA_ROOT, filenames[0])
    else:
        temp_filenames = filenames[0]
        temp_filenames = temp_filenames.split('=')
        if len(temp_filenames) != 2:
            print('Need one and only one filename= to pass in a filename')
            exit(0)
        filename = temp_filenames[1]

        print(f'Using json file passed in as a parameter: {filename}')
        return filename


def process_checker(args, subs):
    '''
    process_checker will check if the process.

    :param args: tuple of arguments sent in
    :type args: tuple
    :param subs: no_import_helper.check_for_batch_args(args, subs) searches for subs in args (a tuple)
    :type subs: str
    :return: empty string or the name of the process.
    :rtype: str
    '''
    possibilities = no_import_helper.check_for_batch_args(args, subs)
    if len(possibilities) != 1:
        return ''
    possibility = possibilities[0]
    process_array = possibility.split('=')
    return process_array[1] if len(process_array) == 2 else ''
