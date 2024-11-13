'''
    Reads a json file creates new paragraphs

:returns: nothing
'''
import os
import sys
import helpers.import_common_class.paragraph_helpers as import_helper
import helpers.no_import_common_class.paragraph_helpers as no_import_helper
import constants.scripts as constants


def run(*args):
    '''
        test the create process use no args
        >>> python manage.py runscript -v3  create_paragraphs --script-args

        run the updates, use updating
        >>> python manage.py runscript -v3  create_paragraphs --script-args updating
    '''
    updating = True if constants.UPDATING in args else False
    filename = filename_checker(args, constants.SCRIPT_PARAM_SUBSTR['filename'])
    print(f'Running paragraph creator with updating == {updating} and filename == {filename}')

    import_helper.paragraph_json_to_db(filename, updating)


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
