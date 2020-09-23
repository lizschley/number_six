'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Make sure you have read and understood process: scripts/documentation/update_process.md

    Three part process (this script is Step 1):
    1. Run this script to read db data and write json to be edited
       * note - see usage directions in run method, below
    2. Start with S1 output data and edit what you want updated and delete the rest
    3. Run batch_json_db_updater_s3 to update the database using the Step 2 file changes


:Output: Writes a json file to be edited or (in the future) used to update production
'''
import os
import sys
import constants.scripts as constants
import helpers.import_common_class.paragraph_helpers as import_helper
import helpers.no_import_common_class.paragraph_helpers as para_helper


def run(*args):
    '''
        Step One Notes
        * Read, understand and follow directions: scripts/documentation/update_process.md
        * Step One only runs in development, since production data comes from development
        * Preparing to run in the actual production environment and preparing to run_as_prod in
          developmment, are the same in in Step One
        * Using the run_as_prod parameter does three things:
          1. it prefixes the output file with <PROD_PROCESS_IND>
          2. add_* file_data input will throw an error (see update_process.md for more information)
          3. creates a dev_id to unique_key table.  This is necessary to handle new associations
             that are not associated with another record update.  For example, say you want to add a
             paragraph to another group or you reallize that you forgot to associate a reference that
             you used.  You may not have the unique key necessary to find the correct paragraph, group
             or reference.
        * If you only want explicit creates (add_* and delete_* keys) and no updates, you can bypass
          step 1 entirely

        Step One Usage
        >>> python manage.py runscript -v3  batch_json_db_updater_s1
        or (to just see printed output of retrievals)
        >>> python manage.py runscript -v3  batch_json_db_updater_s1 --script-args run_as_prod

        Step One Process
            * reads json data from <INPUT_TO_UPDATER_STEP_ONE>
            * copies add_* and delete_* input to the output file without changes
            * writes json file to <MANUAL_UPDATE_JSON> that includes all of the data specified by
              the input (<INPUT_TO_UPDATER_STEP_ONE>)
        Step Two Process
            * manually edit the output from Step 1 (only if not a real production run)
            * If development environment, move the file to <INPUT_TO_UPDATER_STEP_THREE>
            * If production environment <PROD_INPUT_JSON> (should have no manual edits)
    '''
    process_data = init_process_data(args)
    if process_data.get('error'):
        sys.exit(process_data['error'])
    process_data = establish_directories(process_data)
    res = call_process(process_data)
    if res != 'ok':
        print(f'Error! {res}')


def init_process_data(args):
    ''' Gather input parameters and data from file '''
    if os.getenv('ENVIRONMENT') == 'production':
        return {'error': 'This script should only run in the development environment'}
    run_as_prod = constants.RUN_AS_PROD in args
    message = test_for_errors(args, run_as_prod)
    if message != 'ok':
        return {'error': message}
    return {'run_as_prod': run_as_prod}


def test_for_errors(args, run_as_prod):
    'Ensures the correct environment and number of parameters.'
    message = f'Error! Too many args, args == {args}'
    if len(args) > 1:
        return message
    if not run_as_prod and len(args) == 1:
        return message
    return 'ok'


def establish_directories(process_data):
    ''' Establish input and output directories for Step One '''
    process_data['input_directory'] = constants.INPUT_TO_UPDATER_STEP_ONE
    process_data['output_directory'] = constants.MANUAL_UPDATE_JSON
    return process_data


def call_process(process_data):
    ''' Right now only works for Step 1, which always has same input and output directories '''
    files_processed = step_one_process(process_data)
    if files_processed == 0:
        return f'Step 1, no results; 0 Python files in {process_data["input_directory"]}'
    return 'ok'


def step_one_process(process_data):
    ''' passes function with correct calls to common looping through json files function '''
    num = para_helper.loop_through_files_for_db_updates(import_helper.update_paragraphs_step_one,
                                                        process_data)
    return num
