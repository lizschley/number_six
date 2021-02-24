''' Methods that are not specific to Paragraph functionality, but could be useful '''
import os
import shutil
import sys
from decouple import config
from django.utils.text import slugify
import constants.scripts as scripts


def valid_non_blank_string(str_to_check):
    '''
    valid_non_blank_string returns True if str_to_check is a valid string with more than just whitespace

    :param str_to_check: string to check
    :type str_to_check: str
    :return: True if it is a valid string that contains more than whitespace, else False
    :rtype: bool
    '''
    if not str_to_check:
        return False
    try:
        res = str_to_check.isspace()
    except AttributeError:
        return False
    return not res


def slugify_string(input_str):
    '''
    slugify_string slugifies the input string.  This is a convenience method, currently for creating
    reference links for a new reference record in a new paragraph record.

    :param input_str: string to slugify
    :type input_str: str
    :return: slugified version of the input string
    :rtype: str
    '''
    return slugify(input_str)


def archive_files_from_input_directories(include_not_done=True):
    '''
    archive_files_from_input_directories moves the files used for processing input data to
    the archive location

    :param include_done: whether to also move files that haven't been manually moved to done or loaded
    :type include_done: bool, optional
    '''
    in_dirs = scripts.ONLY_DONE_INPUT_DIRECTORIES
    num_processed = 0
    if include_not_done:
        in_dirs += scripts.NOT_DONE_INPUT_DIRECTORIES
    num_processed = 0
    target = config('USED_INPUT_FINAL_DIRECTORY', default='')
    if len(target) < 10:
        sys.exit('Target directory does not exist. Checks USED_INPUT_FINAL_DIRECTORY env variable')
    for dir_path in in_dirs:
        params = {'in_dir': dir_path,
                  'out_dir': target,
                  'check_extension': True,
                  'extensions': ['.json'],
                  'num_processed': num_processed}
        num_processed = loop_through_files_to_move(**params)
    print(f'After looping through the input data, {num_processed} files were moved.')


def loop_through_files_to_move(**kwargs):
    '''
    loop_through_files_to_move moves all the files from input directory to output directory

    :param input_dir_path: directory containing files to loop through, this is a shallow loop.
    :type input_dir_path: str
    :return: number of files that were moved
    :rtype: int
    '''
    input_dir_path = kwargs.get('in_dir')
    output_dir_path = kwargs.get('out_dir')
    check_extension = kwargs.get('check_extension', False)
    extensions = kwargs.get('extensions')
    num_processed = kwargs.get('num_processed', 0)
    for filename in os.listdir(input_dir_path):
        if check_extension and filename not in extensions:
            continue
        output_path = os.path.join(output_dir_path, filename)
        input_path = os.path.join(input_dir_path, filename)
        shutil.move(input_path, output_path)
        num_processed += 1
    return num_processed


def copy_file_from_source_to_target(source, target):
    '''
    copy_file_from_source_to_target to target.  Both source and target should have
    a complete file_path

    :param source: path to source file path
    :param target: path to target file path
    '''

    try:
        shutil.copyfile(source, target)
    except IOError as err:
        print(f'Unable to copy file from {source} to {target}')
        sys.exit(f'Error: {err}')


def replace_line(**kwargs):
    ''' replace_line replaces one line in the base.html file '''
    with open(kwargs['in_file']) as fin, open(kwargs['out_file'], 'w') as fout:
        for line in fin:
            lineout = line
            if kwargs['sub_str'] in line:
                lineout = f'{kwargs["new_line"]}\n'
            fout.write(lineout)
