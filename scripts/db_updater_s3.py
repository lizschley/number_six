'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Make sure you have read and understood process: scripts/documentation/update_process.md

    Three part process (this is Step 3):
    1. Prepare input, then run scripts/db_updater_s1.py
    2. Start with Step 1 output data and edit what you want updated and delete the rest
    3. Run this script to update the database using the Step 2 file changes
        (run method has usage information)

:returns: nothing
'''
import sys
from decouple import config
from common_classes.para_db_update_process import ParaDbUpdateProcess
from common_classes.para_db_update_process_prod import ParaDbUpdateProcessProd
import constants.scripts as constants
import helpers.import_common_class.paragraph_helpers as import_helper
import helpers.no_import_common_class.paragraph_helpers as para_helper


def run(*args):
    '''
        Step Three Usage:
            * Note - designed to run in development or production
            * IMPORTANT - using for_prod in step 3 is ONLY for testing. It will error out in production

        1. Make sure you have input created and edited correctly in Steps 1 and 2
            * See scripts/db_updater_s1.py
                and scripts/documentation/update_process.md for details
            * Edited input must be in one of the following directories (see constants.scripts.py):
            ***  <PROD_INPUT_JSON > (for production updates or testing) or
            ***  <INPUT_TO_UPDATER_STEP_THREE> (for development updates)
            * if you are updating development with the for_prod parameter, the filename
                must have constants.PROD_PROCESS_IND as a prefix (use for_prod argument when in step 1)

        2. Run this script, possible parameters
        >>> python manage.py runscript -v3 db_updater_s3
        or
        >>> python manage.py runscript -v3 db_updater_s3 --script-args updating
        or
        >>> python manage.py runscript -v3 db_updater_s3 --script-args for_prod
        or
        >>> python manage.py runscript -v3 db_updater_s3 --script-args for_prod updating

        Notes on Arguments
        * No updating - will process the input data as much as it can without updating; prints to aid
                        in testing.
        * updating - will process the input data, doing updates.
        * if NOT for_prod, will use the ParaDbUpdateProcess class (won't work in production environment)
        * for_prod (or in the production environment) - will use the ParaDbUpdateProcessProd class
                     will error out if Step 1 hasn't been run with for_prod parameter (creates lookup)
                     will error out if you use add_* as an input key
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
    updating = False
    for_prod = False
    if constants.FOR_PROD in args:
        for_prod = True
    if constants.UPDATING in args:
        updating = True
    message = test_for_errors(args, for_prod, updating)
    if message != 'ok':
        return {'error': message}
    return switches_from_args(updating, for_prod)


def test_for_errors(args, for_prod, updating):
    'Ensures the correct number and combinations of parameters.'
    message = f'Error! To many args or wrong args, args == {args}'
    if len(args) > 2:
        return message
    if len(args) == 2 and (not updating or not for_prod):
        return message
    if for_prod and config('ENVIRONMENT') == 'production':
        return f'Invalid parameter (for_prod) for production environment, args == {args} '
    return 'ok'


def switches_from_args(updating, for_prod):
    ''' Return from init process data '''
    return {
        'updating': updating,
        'for_prod': for_prod,
    }


def establish_input_directory(process_data):
    ''' The process and files depend on the process data '''
    if config('ENVIRONMENT') == 'production':
        process_data['input_directory'] = constants.PROD_INPUT_JSON
        process_data['class'] = ParaDbUpdateProcessProd
    elif config('ENVIRONMENT') == 'development':
        process_data['input_directory'] = constants.INPUT_TO_UPDATER_STEP_THREE
        process_data['class'] = development_update_class(process_data)
    else:
        return {'error': (f'Could not select input directory, process data=={process_data}, '
                          f'and enironment = {config("ENVIRONMENT")}')}
    return process_data


def development_update_class(process_data):
    ''' Allows testing prod update before there was a prod '''
    if process_data['for_prod']:
        return ParaDbUpdateProcessProd
    return ParaDbUpdateProcess


def call_process(process_data):
    ''' Right now only works for Step 1, which always has same input and output directories '''
    files_processed = step_three_process(process_data)
    if files_processed == 0:
        return f'Step 3, no {prod_or_dev(process_data)} in {process_data["input_directory"]}'
    return 'ok'


def prod_or_dev(process_data):
    ''' Returns different message based on the process_data '''
    env = config('ENVIRONMENT')
    if process_data['for_prod']:
        return f'production-like files to use for updating, env=={env}'
    return f'development files to use for updating, env=={env}'


def step_three_process(process_data):
    ''' passes function with correct calls to common looping through json files function '''
    num = para_helper.loop_through_files_for_db_updates(import_helper.update_paragraphs_step_three,
                                                        process_data)
    return num
