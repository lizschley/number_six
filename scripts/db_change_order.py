'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Make sure you have read and understood process: scripts/documentation/update_process.md

    Three part process (this is Step 3):
    1. copy and edit json to be edited, then run scripts/db_updater_s1.py
    2. Start with Step 1 output data and edit what you want updated and delete the rest
    3. Run this script to update the database using the Step 2 file changes
        (run method has usage information)

:returns: nothing
'''
import sys
from decouple import config
import constants.scripts as constants
import helpers.import_common_class.paragraph_helpers as import_helper
import helpers.no_import_common_class.paragraph_helpers as para_helper
from common_classes.para_db_update_order import ParaDbUpdateOrder


def run(*args):
    '''
        Step Three Usage:
            * Note - designed to run in development only

        1. Make sure you have input created and edited correctly in Steps 1 and 2
            * See scripts/db_updater_s1.py
                and scripts/documentation/update_process.md for details
            * The edited input must have been moved to one of the following directories (see constants):
            ***  <INPUT_TO_UPDATER_STEP_THREE>

        2. Run this script, possible parameters
        >>> python manage.py runscript -v3 db_change_order --script-args
        or
        >>> python manage.py runscript -v3 db_change_order --script-args updating

        Notes on Arguments
        * No arguments - will not do any db updates.
        * updating (only) - will process the input data, doing updates.
    '''
    process_data = init_process_data(args)
    if process_data.get('error'):
        sys.exit(process_data['error'])
    process_data = establish_input_directory(process_data)
    if process_data.get('error'):
        sys.exit(process_data['error'])
    num_files = call_process(process_data)
    print(f'update the order for groups or paragraphs: number of files: {num_files}')


def init_process_data(args):
    ''' Gather information for Step Three, in order to update the database '''
    updating = False
    if constants.FOR_PROD in args:
        return f'{constants.FOR_PROD} is invalid for this process'
    if constants.UPDATING in args:
        updating = True
    message = test_for_errors(args, updating)
    if message != 'ok':
        return {'error': message}
    return switches_from_args(updating)


def test_for_errors(args, updating):
    'Ensures the correct number and combinations of parameters.'
    message = f'Error! To many args or wrong args, args == {args}'
    if len(args) > 1:
        return message
    if len(args) == 1 and not updating:
        return message
    if config('ENVIRONMENT') != 'development':
        return 'This process is a development only process'
    return 'ok'


def switches_from_args(updating):
    ''' Return from init process data '''
    return {
        'updating': updating,
    }


def establish_input_directory(process_data):
    ''' The process and files depend on the process data '''
    process_data['input_directory'] = constants.INPUT_TO_UPDATER_STEP_THREE
    process_data['class'] = ParaDbUpdateOrder
    return process_data


def call_process(process_data):
    ''' passes function with correct calls to common looping through json files function '''
    num = para_helper.loop_through_files_for_db_updates(import_helper.update_paragraphs_update_order,
                                                        process_data)
    return num
