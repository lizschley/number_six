'''
    Reads a json file and either displays how it looks after basic paragraph processing
    or creates new paragraphs

:returns: nothing
'''
import os
import sys
from pprint import pprint
import helpers.import_common_class.paragraph_helpers as import_helper
import helpers.no_import_common_class.paragraph_helpers as no_import_helper
import constants.scripts as constants


def run(*args):
    '''
        For simply creating and displaying input, no args, though you can specify filename:
        >>> python manage.py runscript -v3  batch_json_processor --script-args
            filename=/Users/liz/development/number_six/data/data_for_creates/loaded/chinese_holly_load.json
        or
        >>> python manage.py runscript -v3  batch_json_processor (picks first json file in directory)

        To either do or test the create process, use the following args:
        >>> python manage.py runscript -v3  batch_json_processor --script-args process=db_update
        >>> python manage.py runscript -v3  batch_json_processor --script-args process=test_update
    '''
    filename = filename_checker(args, constants.SCRIPT_PARAM_SUBSTR['filename'])
    print(f'filename == {filename}')

    process = process_checker(args, constants.SCRIPT_PARAM_SUBSTR['process'])
    print(f'process=={process}')
    if process in (constants.DB_UPDATE, constants.TEST_UPDATE):
        updating = process == constants.DB_UPDATE
        print(f'Running paragraph creator with updating == {updating}')
        import_helper.paragraph_json_to_db(filename, updating)
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
    print(f'args type is {type(args)} args=={args}')
    filenames = no_import_helper.check_for_batch_args(args, subs)
    if len(filenames) > 1:
        # if passing > 1 argument that passes extension test
        sys.exit('Have not implemented passing in > one specific filename and path.')
    elif len(filenames) < 1:
        # if no arguments, get first filename that passes extension test in correct directory
        # could do in a loop, but extra work unless reason presents itself
        filenames = no_import_helper.check_for_batch_args(os.listdir(constants.INPUT_CREATE_JSON), subs)
        if len(filenames) < 1:
            sys.exit('No json files in default directory and no json file as input parameter')
        return os.path.join(constants.INPUT_CREATE_JSON, filenames[0])
    else:
        temp_filenames = filenames[0]
        temp_filenames = temp_filenames.split('=')
        if len(temp_filenames) != 2:
            sys.exit('Need one and only one filename= to pass in a filename')
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
