'''
    ref: https://django-extensions.readthedocs.io/en/latest/runscript.html

    Three part process:
    1. read data, write json to be editted
    2. edit the data manually (only what you want updated, delete the rest)
    3. do the update by reading the file.

:returns: nothing
'''
import os
from portfolio.settings import BASE_DIR

INPUT_TO_UPDATER_STEP_ONE = os.path.join(BASE_DIR, 'data/data_for_updates/dev_input')
INPUT_TO_UPDATER_STEP_THREE = os.path.join(BASE_DIR, 'data/data_for_updates/dev_input_json')
MANUAL_UPDATE_JSON = os.path.join(BASE_DIR, 'data/data_for_updates/dev_manual_json')
PROD_INPUT_JSON = os.path.join(BASE_DIR, 'data/data_for_updates/dev_manual_json')
DEV_INPUT_JSON = os.path.join(BASE_DIR, 'data/data_for_updates/dev_manual_json')
DO_UPDATE = 'do_update'
TEST_UPDATE = 'test_update'
RUN_AS_PROD = 'run_as_prod'
JSON_SUB = '.json'
PY_SUB = '.py'
PROD_PROCESS_IND = 'likeprod'


def run(*args):
    '''
        usage as follows:
        Step 1 - development only, no parameters, exits if prod
        >>> python manage.py runscript -v3  batch_json_db_updater
            * reads python data from <INPUT_TO_UPDATER_STEP_ONE> (Python dictionaries)
            * no production version of this, since production data comes from development
            * writes json file to <MANUAL_UPDATE_JSON>

        Step 2 - development only, manual step to make the changes you want
            * edit json file in <MANUAL_UPDATE_JSON>
            * after editing, manually move json file to <INPUT_TO_UPDATER_STEP_THREE>
            * note - need to change name to include <PROD_PROCESS_IND> if using run_as_prod option

        Step 3 - production or development, this is where db updates happen (can run without updates)

        * Using the run_as_prod as argument - doesn't run anything when its the only argument
        ** will give more create and update possibilities in development as well as in production.
        ** It also allows thorough testing for the production process in development.
        * Do the following in manual edits:
        ** for creates: pull in data using the updated_at date/time input
        ***  then create, edit or delete text, etc as needed
        ***  explicitly set the guid or other unique field
        ***  make the id really high, & be careful to use the same id in associations
        ** for updates: high ids or use the same one; be careful about associations always
        ***   make desired changes
        ***   remember to include <PROD_PROCESS_IND> (value of) in the json file name after editing

        >>> python manage.py runscript -v3  batch_json_db_updater --script-args run_as_prod
            * does not run anything without the do_update or test_update switch
            * reads python data from <INPUT_TO_UPDATER_STEP_THREE>
            *** (checks filename for <PROD_PROCESS_IND>)
            * plan to log any error messages

        * arguments: do_update or test_update
        ** This is the normal process for updates:
        *** with do_update
        ****  Can update, but not create paragraphs (unless you use run_as_prod, which takes thought)
        ****  Can update or create categories, groups and references
        ****  Associations can be added or deleted
        *** with test_update - will do a dry run only, test before updates

        >>> python manage.py runscript -v3  batch_json_db_updater test_update
        or
        >>> python manage.py runscript -v3  batch_json_db_updater test_update run_as_prod
            * reads python data from <INPUT_TO_UPDATER_STEP_THREE>
            *** (ensures filename does not have <PROD_PROCESS_IND>)
            * test process & data ahead of update
            * won't do db updates without the do_update switch
            * plan to log any error messages

        * do update argument - does the db updates, other than that is similar to
        **  test_update & run_as_prod or just test_update
        >>> python manage.py runscript -v3  batch_json_db_updater do_update
        or
        >>> python manage.py runscript -v3  batch_json_db_updater do_update run_as_prod

    '''
    process_data = init_process_data(args)
    if process_data.get('error'):
        print(process_data['error'])
        exit(1)
    process_data = establish_process_and_files(process_data)
    if process_data.get('error'):
        print(process_data['error'])
        exit(1)
    res = call_process(process_data)
    if res != 'ok':
        print(f'Error! {res}')

def init_process_data(args):
    ''' Gather information to do one of the following:
        * report setup errors
        * gather data necessary to start the update process
        * test input data and update process as much as possible without doint any db updates
        * do the db update process
    '''
    do_update = False
    test_update = False
    is_prod = False
    if RUN_AS_PROD in args:
        is_prod = True
    if DO_UPDATE in args:
        do_update = True
    if TEST_UPDATE in args:
        test_update = True
    message = test_for_errors(args, is_prod, do_update, test_update)
    if message != 'ok':
        return {'error': message}
    if not is_prod:
        is_prod = True if os.getenv('ENVIRONMENT') == 'production' else False
    return switches_from_args(is_prod, do_update, test_update)


def test_for_errors(args, is_prod, do_update, test_update):
    message = f'Error! To many args, args == {args}'
    if len(args) > 2:
        return message
    if not is_prod and len(args) > 1:
        return message
    elif is_prod and len(args) == 1:
        return f'For production run you need either do_update or test update, args == {args} '
    if do_update and test_update:
        return f'Error! do_update and test_update conflict, args == {args}'
    return 'ok'


def switches_from_args(is_prod, do_update, test_update):
    return {
        'is_prod': is_prod,
        'do_update': do_update,
        'test_update': test_update,
    }

def establish_process_and_files(process_data):
    if (not process_data.get('db_update') and not process_data.get('is_prod') and
        not process_data.get('is_prod')):
        process_data['input_directory'] = INPUT_TO_UPDATER_STEP_ONE
        process_data['output_directory'] = MANUAL_UPDATE_JSON
        process_data['process'] = 'step_one'
        return process_data

def call_process(process_data):
    if process_data.get('process') and process_data['process'] == 'step_one':
        files_processed = step_one_process(process_data)
        if files_processed == 0:
            return f'Step 1, no results; 0 Python files in {process_data["input_directory"]}'
        print(f'Step 1 processed {files_processed} files, results in {process_data["output_directory"]}')
        return 'ok'
    return 'ok'

def step_one_process(process_data):
    directory = process_data['input_directory']
    num_processed = 0
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            num_processed += 1
            print(f'calling step 1 process with {os.path.join(directory, filename)}')
        else:
            continue
    return num_processed
