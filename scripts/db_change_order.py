'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Run scripts/db_updater_s1.py with json:  {"group_ids": [35]} or {"category_ids": [1]} (examples)

    Follow instructions in run method.

    Note - This script will only change the paragraphs (or group) order, but if you find yourself
    updating the update the paragraph text
    First - delete the group_id or the category_id in the input file:
           (<INPUT_TO_UPDATER_STEP_THREE> (in scripts/constants))
    Then - run the the same input with the db_updater_s3 script

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
        This runs Step Three, which is designed to run in development only

        Prerequisites:
        Step 1. Make sure you have input created and edited correctly in Steps 1 and 2
            Run scripts/db_updater_s1.py with json, example below:
               {"group_ids": [35]} OR {"category_ids": [1]}
            Output will be in <INPUT_TO_UPDATER_STEP_THREE> (in scripts/constants)

        Step 2. Add key "group_id": 35 (group_id from Step One Json file)
                Also keep paragraph list intact:  Need all the records, plus the id, guid and text
                     keep the groupparagraph list intact as well
                     Reorder the paragraph records to be the desired order

                ----> OR <-----

                Add key "category_id": 1 (category_id from Step One Json file)
                Also keep the group list intact
                Reorder the group records to be the desired order

        3. Run this script, possible parameters
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
