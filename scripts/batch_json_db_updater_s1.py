'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Make sure you have read and understood process: scripts/documentation/update_process.md

    Three part process (this script is Step 1):
    1. Run this script to read db data and write json to be edited
       * note - see usage directions in run method, below
    2. Start with S1 output data and edit what you want updated and delete the rest
       * Note - it is possible to bypass this step and send in input parameters to get one record type
                Please see Step One run notes and scripts/documentation/update_process.md
    3. Run batch_json_db_updater_s3 to update the database using the Step 2 file changes


:Output: Writes a json file to be edited or (in the future) used to update production
'''
import os
import sys
import constants.crud as crud
import constants.scripts as constants
import helpers.import_common_class.paragraph_helpers as import_helper
import helpers.no_import_common_class.paragraph_helpers as para_helper
from utilities.record_dictionary_utility import RecordDictionaryUtility


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
          step 1 entirely.  However it can be helpful to run step 1 to get the data needed to do the
          updates (just copy over the template)
        * You can also send in input parameters if you only need to change wording in one record and do
          not need to worry about any of the relational data

        Step One Usage
        >>> python manage.py runscript -v3  batch_json_db_updater_s1
        or to get the run_as_prod variations on the output file
        >>> python manage.py runscript -v3  batch_json_db_updater_s1 --script-args run_as_prod
        to bypass normal Step One processing (which gets related data) and only get one type of record
        >>> python manage.py runscript -v3  batch_json_db_updater_s1 --script-args paragraphs=1,2,3 (ex)
        For complicated one_time retrieval, edit RecordDictionaryUtility.one_time_get_content(out_dir):
        >>> python manage.py runscript -v3  batch_json_db_updater_s1 --script-args one_time=true


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
    if process_data.get('bypassed'):
        sys.exit(f'Sucessfully bypassed process, check {constants.MANUAL_UPDATE_JSON}')
    if process_data.get('error'):
        sys.exit(process_data['error'])
    process_data = establish_directories(process_data)
    res = call_process(process_data)
    if res != 'ok':
        print(f'Error! {res}')


def init_process_data(args):
    ''' Gather input parameters and data from file '''
    if os.getenv('ENVIRONMENT') != 'development':
        return {'error': 'This script should only run in the development environment'}
    run_as_prod = constants.RUN_AS_PROD in args
    params = process_other_args(args, run_as_prod)
    if params['message'] != 'ok':
        return {'error': params['message']}
    if params.get('bypass_step1_prep'):
        params.pop('bypass_step1_prep')
        if params['params']['key'] == 'one_time':
            RecordDictionaryUtility.one_time_get_content(constants.MANUAL_UPDATE_JSON)
        else:
            RecordDictionaryUtility.create_json_list_of_records(constants.MANUAL_UPDATE_JSON, params)
        return {'bypassed': True}
    return {'run_as_prod': run_as_prod}


def process_other_args(args, run_as_prod):
    'Ensures the correct environment and number of parameters.'
    message = f'Error! Too many args, args == {args}'
    if len(args) > 1:
        return {'message': message}
    if not run_as_prod and len(args) == 1:
        params = validate_input(args[0])
        print(f'Bypassing relational process with these args: {args}')
        return {'message': 'ok', 'bypass_step1_prep': True, 'params': params}
    return {'message': 'ok'}


def validate_input(args):
    ''' create dictionary from args if it is valid '''
    print(f'args == {args}, type={type(args)}')
    res = check_input(args)
    print(f'res=={res}')
    return res


def check_input(args):
    ''' test validity of args, error out if things don't check out '''
    temp = args.split('=')
    if len(temp) != 2:
        sys.exit(f'Error: Wrong input variables, should be key=value, but is {args}')
    if temp[0] == 'one_time':
        pass
    elif temp[0] not in crud.UPDATE_DATA.keys():
        sys.exit(f'Error: key (left of =) should be in {crud.UPDATE_DATA.keys()}, but is {args}')
    return {'key': temp[0], 'select_criteria': temp[1]}


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
