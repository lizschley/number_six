import os
import sys
import json
from pprint import pprint

from portfolio.settings import BASE_DIR
import constants.common as cc
from common_classes.paragraphs_for_display import ParagraphsForDisplay

JSON_DATA_ROOT = os.path.join(BASE_DIR, os.getenv('JSON_DATA'))


# usage as follows:
# > python manage.py runscript -v3  batch_json_processor --script-args  /Users/liz/development/number_six/test/test.json
# or > python manage.py runscript -v3  batch_json_processor
def run(*args):
    # this gives you runscript
    print(f'args == {sys.argv[1]}')
    # this gives you filename
    print(f'args == {args}')
    filename = filename_checker(args)
    print(f'filename == {filename}')
    # Opening JSON file
    f = open(filename, 'r')
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    print(data)
    paragraphs = ParagraphsForDisplay()
    paragraph_list = paragraphs.json_to_paragraph_list(data)
    pprint(paragraph_list)
    # Closing file
    f.close()
    # after creating db records, we should move the file to the loaded directory


def filename_checker(filename):
    filenames = check_extension(filename)
    if len(filenames) > 1:
        # if passing > 1 argument that passes extension test
        print('Have not implemented passing in > one specific filename and path.')
        exit(0)
    elif len(filenames) < 1:
        # if no arguments, get first filename that passes extension test in correct directory
        # could do in a loop, but extra work unless reason presents itself
        print('Taking first file with a json extension from the default data directory')
        filenames = check_extension(os.listdir(JSON_DATA_ROOT))
        if len(filenames) < 1:
            print('No json files in default directory and no json file as input parameter')
            exit(0)
        return os.path.join(JSON_DATA_ROOT, filenames[0])
    else:
        print(f'Using json file passed in as a parameter: {filenames[0]}')
        return filenames[0]


def check_extension(filenames):
    subs = cc.SCRIPT_PARAM_SUBSTR['filename']
    return [i for i in filenames if subs in i]