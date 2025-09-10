''' Methods that are not specific to Paragraph functionality, but could be useful '''
import csv
import os
import shutil
import sys
import constants.utilities as utilities
import random_methods as utils


def archive_files_from_input_directories(**kwargs):
    '''
    Note - these paths do not currently exist, but I found this very useful

    archive_files_from_input_directories moves the files used for processing input data to
    the archive location

    It offers the option to exclude certain directories.  This is driven by kwargs and constants

    :param include_done: whether to also move files that haven't been manually moved to done or loaded
    :type include_done: bool, optional
    '''
    in_dirs = utilities.ALWAYS_ARCHIVE_INPUT_DIRECTORIES
    num_processed = 0
    if utils.key_not_in_dictionary(kwargs, 'exclude_not_done'):
        in_dirs += utilities.NOT_DONE_INPUT_DIRECTORIES
    if utils.key_not_in_dictionary(kwargs, 'exclude_prod'):
        in_dirs.append(utilities.PROD_INPUT_DIRECTORY)
    if utils.key_not_in_dictionary(kwargs, 'target'):
        sys.exit('Target directory does not exist. must be passed using the kwargs key "target"')
    else:
        target = kwargs['target']

    for dir_path in in_dirs:
        params = {'in_dir': dir_path,
                  'out_dir': target,
                  'extensions': ['json'],
                  'num_processed': num_processed}
        num_processed = loop_through_files_to_move(**params)
    return num_processed


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
    extensions_to_delete = kwargs.get('extensions')
    num_processed = kwargs.get('num_processed', 0)
    for filename in os.listdir(input_dir_path):
        if not delete_file(filename, extensions_to_delete):
            continue
        input_path = os.path.join(input_dir_path, filename)
        output_path = os.path.join(output_dir_path, filename)
        move_file(input_path, output_path)
        num_processed += 1
    return num_processed


# path includes filename
def move_file(input_path, output_path):
    shutil.move(input_path, output_path)


def delete_file(filename, extensions_to_delete):
    '''
    delete_file return True if the file extension is included in extensions_to_delete
    otherwise False

    :param filename: filename that may be deleted
    :type filename: str
    :param extensions_to_delete: extension for temporary files you want to delete
    :type extensions_to_delete: list or tuple
    :return: True if you want to delete the file, else False
    :rtype: bool
    '''
    do_delete = False
    temp = filename.split('.')
    if len(temp) != 2:
        return do_delete
    for ext in extensions_to_delete:
        if ext == temp[1]:
            do_delete = True
    return do_delete


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


def dictionary_list_from_csv(filepath):
    ''' generate a list of dictionaries from a csv file '''
    return_list = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        return_list = list(reader)
    return return_list


def file_path_with_extension(directory, ext):
    ''' simple retrieve file with given extension in given directory '''
    for filename in os.listdir(directory):
        if use_file(filename, ext):
            file_path = os.path.join(directory, filename)
            return file_path
        continue
    return None


def use_file(filename, ext):
    ''' ensure file extension is correct '''
    temp = filename.split('.')
    if temp[-1] == ext:
        return True
    return False


# untested
def write_file_from_string(input, filepath, mode='w'):
    with open(filepath, mode) as file:
        file.write(input)


def append_file_from_array(line, filepath, mode='a+'):
    with open(filepath, mode) as file:
        file.write(f"{line}\n")
