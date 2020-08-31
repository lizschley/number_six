''' Script constants '''
import os
from portfolio.settings import BASE_DIR

# input parameters
RUN_AS_PROD = 'run_as_prod'
UPDATING = 'updating'
DB_UPDATE = 'db_update'
TEST_UPDATE = 'test_update'

# substrings
JSON_SUB = '.json'
PY_SUB = '.py'
SCRIPT_PARAM_SUBSTR = {'filename': '.json', 'process': 'process=', }

# directories
INPUT_CREATE_JSON = os.path.join(BASE_DIR, 'data/data_for_creates')
INPUT_TO_UPDATER_STEP_ONE = os.path.join(BASE_DIR, 'data/data_for_updates/dev_input')
INPUT_TO_UPDATER_STEP_THREE = os.path.join(BASE_DIR, 'data/data_for_updates/dev_input_json')
MANUAL_UPDATE_JSON = os.path.join(BASE_DIR, 'data/data_for_updates/dev_manual_json')
PROD_INPUT_JSON = os.path.join(BASE_DIR, 'data/data_for_updates/prod_input_json')

# filename prefixes
PROD_PROCESS_IND = 'likeprod_'
