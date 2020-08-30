'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Three part process (this is Step 1):
    1. Run this script to read db data and write json to be edited
       * note - see usage directions in run method, below
    2. Start with S1 output data and edit what you want updated and delete the rest
    3. Run batch_json_db_updater_s3 to update the database using the Step 2 file changes

:Output: Writes a json file to be edited or (in the future) used to update production
'''
import os
import sys
from portfolio.settings import BASE_DIR


INPUT_TO_UPDATER_STEP_ONE = os.path.join(BASE_DIR, 'data/data_for_updates/dev_input')
MANUAL_UPDATE_JSON = os.path.join(BASE_DIR, 'data/data_for_updates/dev_manual_json')
UPDATING = 'updating'
JSON_SUB = '.json'
PY_SUB = '.py'
PROD_PROCESS_IND = 'likeprod'


def run(*args):
    '''
        Usage as follows:
            * Note - no production version of this, since production data comes from development

        Step One Usage - runs in development only
            1. Copy data/dictionary_templates/starting_dev_process_input.py
            2. Move the copy to <INPUT_TO_UPDATER_STEP_ONE> (see above)
            3. Read the file you just copied to understand what you need as input and then gather
               the necessary information
            4. Following the directions, edit the input file for desired results
            5. Once the input is correct, run this script.

            * Note - If no parameters: groups, references and categories will not be created

        >>> python manage.py runscript -v3  batch_json_db_updater updating
        or
        >>> python manage.py runscript -v3  batch_json_db_updater

        Step One Process
            * reads python data from <INPUT_TO_UPDATER_STEP_ONE> (Python dictionary)
            * creates category, group, or refererence records (if updating)
            * writes json file to <MANUAL_UPDATE_JSON> that includes all of the data specified by
              the input (<INPUT_TO_UPDATER_STEP_ONE>)
    '''
    process_data = init_process_data(args)
    if process_data.get('error'):
        print(process_data['error'])
        sys.exit(process_data['error'])
    process_data = establish_directories(process_data)
    if process_data.get('error'):
        print(process_data['error'])
        sys.exit(process_data['error'])
    res = call_process(process_data)
    if res != 'ok':
        print(f'Error! {res}')


def init_process_data(args):
    ''' Gather input parameters and data from file '''
    if UPDATING in args:
        updating = True
    is_prod = os.getenv('ENVIRONMENT') == 'production'
    message = test_for_errors(args, updating, is_prod)
    if message != 'ok':
        return {'error': message}
    return {}


def test_for_errors(args, updating, is_prod):
    'Ensures the correct environment and number of parameters.'
    message = f'Error! To many args, args == {args}'
    if len(args) > 1:
        return message
    if not updating and len(args) == 1:
        return message
    if is_prod:
        return f'For production run you need either do_update or test update, args == {args} '
    return 'ok'


def establish_directories(process_data):
    ''' Establish input and output directories for Step One '''
    process_data['input_directory'] = INPUT_TO_UPDATER_STEP_ONE
    process_data['output_directory'] = MANUAL_UPDATE_JSON
    return process_data


def call_process(process_data):
    ''' Right now only works for Step 1, which always has same input and output directories '''
    files_processed = step_one_process(process_data)
    if files_processed == 0:
        return f'Step 1, no results; 0 Python files in {process_data["input_directory"]}'
    print(f'Step 1 processed {files_processed} files, results in {process_data["output_directory"]}')
    return 'ok'


def step_one_process(process_data):
    ''' Loops through files in directory and processes each individually '''
    directory = process_data['input_directory']
    num_processed = 0
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            num_processed += 1
            print(f'calling step 1 process with {os.path.join(directory, filename)}')
        else:
            continue
    return num_processed
