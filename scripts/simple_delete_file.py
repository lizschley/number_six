import os
import utilities.file_utils as utils

DIR_PATH = '/Users/eaffie/development/number_six/upload_to_s3/hawaii'
FILE_TO_DELETE = '/Users/eaffie/development/number_six/upload_to_s3/hawaii/airplane_daytime.png'


def delete_from_dir(dirpath):
    num_deleted = 0
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        simple_delete(filepath)
    print(f'Number of files deleted == {num_deleted}')


def simple_delete(filepath):
    print(f'Filename to delete == {filepath}')
    utils.simple_delete(filepath)


if __name__ == '__main__':
    # simple_delete(FILE_TO_DELETE)
    delete_from_dir(DIR_PATH)
