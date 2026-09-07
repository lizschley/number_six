import os
import utilities.file_utils as utils

# DIR_PATH Necessary for all all functions, EXCEPT simple_delete, which is silly to use
DIR_PATH = '/Users/eaffie/Documents/docs_compare_for_github'
# DIR_PATH = '/Users/eaffie/development/misc_js_ts/appscript_methods'
# DIR_PATH = '/Users/eaffie/development/misc_js_ts/classes'

# if / else so only the first true will be implemented

PRINT_FILE_NAMES = True
PRINT_FILE_PATH_PLUS_NAMES = False
DELETE_FILES_IN_DIRECTORY = False


def files_in_dir(dirpath):
    num_deleted = 0
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        if PRINT_FILE_NAMES:
            print(filename)
        elif PRINT_FILE_PATH_PLUS_NAMES:
            print(filepath)
        elif DELETE_FILES_IN_DIRECTORY:
            simple_delete(filepath)
    print(f'Number of files deleted == {num_deleted}')


def simple_delete(filepath):
    # must send full path + name
    print(f'File to delete == {filepath}')
    utils.simple_delete(filepath)


if __name__ == '__main__':
    files_in_dir(DIR_PATH)
