'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Update S3 using the StaticFiles class which inherites from AwsAutomater

    Goal: make updating S3 with new versions and deleting the S3 versions a seamless process.

    Danger: Must make sure NOT to delete the file version that is being used in production. Eventually
            plan to automate this.  

    For now deleting files on S3 is a totally manual process.  Even when I implement automation that
    includes deleting the old S3 files, it is vital to keep the mistakes easily recoverable, by
    versioning with google and github

    Note - images are not versioned and I have no plans to do so.  If I want to replace one will name
           it something different and manually delete the old one.
'''
import sys
from common_classes.static_files import StaticFiles
import constants.scripts as constants


def run(*args):
    '''
        Usage:
        Run this script, comma delimited list with no spaces is one argument, will be split into
                         s3_data_keys (List) (only use s3 keys corresponding to updated files that need
                         to be uploaded to S3)

        >>> python manage.py runscript -v3 s3_updater --script-args css,flashcard,cat,script,image

        or (order matters.  home must come second or not be included at all)

        >>> python manage.py runscript -v3 s3_updater --script-args css,flashcard,cat,script,image home

        Notes on Arguments (order matters)
        * No S3 keys - will error out
        * Parameter ONE: css,flashcard,cat,script,image <<--- edit argument (will create list of s3 keys)
            Create a new StaticFiles object once and then loop through the parameters. Each parameter
            corresponds to a key in constants/s3_data keys
            Important
                1. Delete unneeded arguments or will load unchanged css or js file with a new version.
                2. Image files must be copied into the upload_to_s3 folder (will loop through them
                   all.  *** only handles .jpg and .png extensions)
        * Parameter TWO: home - all images will be given the static/home/ prefix.
                         static/projects/ is the default (means the image path is stored in db)
    '''
    data = init_process_data(args)
    print(f'After init_process, data == {data}')
    load_static_files_to_s3(data)


def init_process_data(args):
    '''
    init_process_data errors out if data seems wrong  Otherwise returns data to be loaded to S3

    :param args: passed in arguments
    :type args: tuple
    :return: input data validated and turned into dictionary
    :rtype: dictionary
    '''
    data = {}
    if len(args) == 0:
        sys.exit(f'Error!  Need at least one s3 data key: {constants.S3_DATA_KEYS}')

    data['s3_data_list'] = args[0].split(',')

    if len(args) == 2 and args[1] == constants.HOME:
        data['is_home'] = True
    else:
        data['is_home'] = False
    if not input_ok(data):
        sys.exit(f'Error!  Data not as expected: {data}.  Reread Usage and Notes above.')
    return data


def input_ok(data):
    '''
    input_ok checks to make sure all of the keys derived from first argument are valid s3 data keys

    :param data: should include a dictionary with a s3_data_list key
    :type data: dictionary key == 's3_data_list'; iterable list of valid strings
    :return: True if each value is itemized in constants.S3_DATA_KEYS else False
    :rtype: boolean
    '''
    for key in data['s3_data_list']:
        if key not in constants.S3_DATA_KEYS:
            return False
    return True


def load_static_files_to_s3(data):
    '''
    load_static_files_to_s3 iterates through list of s3 data keys and imports the updated file to S3

    :param data: data passed in through arguments and turned into kwargs
    :type data: dictionary
    '''
    for key in data['s3_data_list']:
        importer = StaticFiles()
        kwargs = input_to_static_files(key, data['is_home'])
        print(f'Running load static files to S3 these arguments: {kwargs}')
        importer.file_upload_process(**kwargs)


def input_to_static_files(s3_data_key, is_home):
    '''
    input_to_static_files sent into StaticFiles.file_upload_process(**kwargs)

    :param s3_data_key: one S3 Data key
    :type s3_data_key: str
    :param is_home: whether use the static/home/ or static/projects prefix for S3 impage object uploads
    :type is_home: bool
    :return: input values needed for S3 file_uploads
    :rtype: dictionary
    '''
    return {
        's3_data_key': s3_data_key,
        'is_home': is_home
    }
