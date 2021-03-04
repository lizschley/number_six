'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Archive dev input
'''
import sys
import utilities.random_methods as utils

def run(*args):
    '''
        Usage:
        Two possibilities: 1. Archive all non-production input data files.  2. Exclude files that
        have not been moved to the done directory.

        The default, meaning no script args, is to archive even the input files that have not been
        removed to the done folder.  This is currently a manual process, because of the
        iterative nature of editing files or in case there was an error.

        If you know there is an input file that you want to keep, just move it from the done file
        and run with the exclude_not_done argument

        I do not archive production input, since the archive directory is not on the EC2 server

        >>> python manage.py runscript -v3 s3_updater --script-args
        or
        >>> python manage.py runscript -v3 archive_dev_input --script-args exclude_not_done
    '''
    if len(args) > 1:
        sys.exit(f'Error! Too many args {args}')

    if len(args) == 0:
        num_processed = utils.archive_files_from_input_directories()
    elif args[0] == 'exclude_not_done':
        num_processed = utils.archive_files_from_input_directories(False)
        print('Excluded input files that had not been moved to the done folder')

    if num_processed is None:
        sys.exit(f'Invalid argument: {args}.')

    sys.exit(f'After looping through the input data, {num_processed} files were moved.')


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
