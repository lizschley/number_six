'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Make sure you have read and understood process: scripts/documentation/update_process.md

    Three part process (this is Step 3):
    1. copy and edit json to be edited, then run scripts/batch_json_db_updater_s1.py
    2. Start with Step 1 output data and edit what you want updated and delete the rest
    3. Run this script to update the database using the Step 2 file changes
        (run method has usage information)

:returns: nothing
'''
import os
import sys
import constants.scripts as constants
import helpers.import_common_class.paragraph_helpers as import_helper
import helpers.no_import_common_class.paragraph_helpers as para_helper


def run(*args):
    '''
        Step Three Usage:
            * Note - designed to run in development or production

        1. Make sure you have input created and edited correctly in Steps 1 and 2
            * See scripts/batch_json_db_updater_s1.py
                and scripts/documentation/update_process.md for details
            * The edited input must have been moved to one of the following directories (see constants):
            ***  <PROD_INPUT_JSON > (for production updates) or
            ***  <INPUT_TO_UPDATER_STEP_THREE> (for run_as_prod and regular updates)
            * if you are updating development with the run_as_prod parameter, the filename
                must have constants.PROD_PROCESS_IND as a prefix (happens automatically if using
                updated_at as an input)

        2. Run this script, possible parameters
        >>> python manage.py runscript -v3  batch_json_db_updater_s3
        or
        >>> python manage.py runscript -v3  batch_json_db_updater_s3 --script-args updating
        or
        >>> python manage.py runscript -v3  batch_json_db_updater_s3 --script-args run_as_prod
        or
        >>> python manage.py runscript -v3  batch_json_db_updater_s3 --script-args run_as_prod updating

        Notes on Arguments
        * No arguments - will process the input data as much as it can without updating; prints to aid
                         in testing.
        * updating (only) - will process the input data, doing updates.
        * run_as_prod - will process the input data as much as it can without updating, will give
                        errors if there is data that came from any other input than date
        * updating run_as_prod (both) - will process the data, if there are no errors, doing updates
    '''
    process_data = init_process_data(args)
    if process_data.get('error'):
        sys.exit(process_data['error'])
    process_data = establish_input_directory(process_data)
    if process_data.get('error'):
        sys.exit(process_data['error'])
    res = call_process(process_data)
    if res != 'ok':
        print(f'Error! {res}')


def init_process_data(args):
    ''' Gather information for Step Three, in order to update the database '''
    is_prod = False
    updating = False
    run_as_prod = False
    if constants.RUN_AS_PROD in args:
        run_as_prod = True
    if constants.UPDATING in args:
        updating = True
    message = test_for_errors(args, run_as_prod, updating)
    if message != 'ok':
        return {'error': message}
    if run_as_prod or os.getenv('ENVIRONMENT') == 'production':
        is_prod = True
    return switches_from_args(is_prod, updating, run_as_prod)


def test_for_errors(args, run_as_prod, updating):
    'Ensures the correct number and combinations of parameters.'
    message = f'Error! To many args or wrong args, args == {args}'
    if len(args) > 2:
        return message
    if len(args) == 2 and (not updating or not run_as_prod):
        return message
    if run_as_prod and os.getenv('ENVIRONMENT') == 'production':
        return f'Invalid parameter (run_as_prod) for production environment, args == {args} '
    return 'ok'


def switches_from_args(is_prod, updating, run_as_prod):
    ''' Return from init process data '''
    return {
        'is_prod': is_prod,
        'updating': updating,
        'run_as_prod': run_as_prod,
    }


def establish_input_directory(process_data):
    ''' The process and files depend on the process data '''
    if os.getenv('ENVIRONMENT') == 'development':
        process_data['input_directory'] = constants.INPUT_TO_UPDATER_STEP_THREE
    elif os.getenv('ENVIRONMENT') == 'production':
        process_data['input_directory'] = constants.PROD_INPUT_JSON
    else:
        return {'error': (f'Could not select input directory, process data=={process_data}, '
                          f'and enironment = {os.getenv("ENVIRONMENT")}')}
    return process_data


def call_process(process_data):
    ''' Right now only works for Step 1, which always has same input and output directories '''
    files_processed = step_three_process(process_data)
    if files_processed == 0:
        return f'Step 3, no updatess; 0 Python files in {process_data["input_directory"]}'
    return 'ok'

def step_three_process(process_data):
    ''' passes function with correct calls to common looping through json files function '''
    num = para_helper.loop_through_files_for_db_updates(import_helper.update_paragraphs_step_three,
                                                        process_data)
    return num