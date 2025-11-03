# defining a function return the current time

import time
import os


def show_time():
    return time.ctime()


def list_files():
    # Get the list of all files and directories
    path = "/Users/eaffie/development/number_six/hawaii/photos"
    dir_list = os.listdir(path)
    print("Files and directories in '", path, "' :")
    # prints all files
    for fn in dir_list:
        print(fn)


if __name__ == '__main__':
    # print(show_time())
    list_files()
