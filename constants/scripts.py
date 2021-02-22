''' Script constants '''
import os
from portfolio.settings import BASE_DIR

# db script arguments
RUN_AS_PROD = 'run_as_prod'
UPDATING = 'updating'
DB_UPDATE = 'db_update'
TEST_UPDATE = 'test_update'

# s3 updater script argurments
HOME = 'home'
DELETE = 'delete'
S3_DATA_KEYS = ['css', 'flashcard', 'cat', 'script', 'image']

# substrings
JSON_SUB = '.json'
PY_SUB = '.py'
SCRIPT_PARAM_SUBSTR = {'filename': '.json', 'process': 'process=', }

# directories
INPUT_CREATE_JSON = os.path.join(BASE_DIR, 'data/data_for_creates')
INPUT_TO_UPDATER_STEP_ONE = os.path.join(BASE_DIR, 'data/data_for_updates/dev_input_step_one')
INPUT_TO_UPDATER_STEP_THREE = os.path.join(BASE_DIR, 'data/data_for_updates/dev_input_step_three')
MANUAL_UPDATE_JSON = os.path.join(BASE_DIR, 'data/data_for_updates/dev_manual_json')
PROD_INPUT_JSON = os.path.join(BASE_DIR, 'data/data_for_updates/prod_input_json')

# filename prefixes
PROD_PROCESS_IND = 'prod_input_'
DEFAULT_PREFIX = 'input_'

# used in utilities.random methods to clear out data, to make things be easier to work with
ONLY_DONE_INPUT_DIRECTORIES = ['data/data_for_updates/dev_input_step_one/done',
                               'data/data_for_updates/dev_input_step_three/done',
                               'data/data_for_creates/loaded'
                               ]
NOT_DONE_INPUT_DIRECTORIES = ['data/data_for_updates/dev_input_step_one',
                              'data/data_for_updates/dev_input_step_three',
                              'data/data_for_creates']
