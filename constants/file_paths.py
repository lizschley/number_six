'''File path constants used for non-test data.'''

import os
import portfolio.settings as settings

if os.getenv('ENVIRONMENT') == 'production':
    DEMO_PARAGRAPH_JSON = os.path.join(settings.BASE_DIR, 'data/demo/urban_coyotes.json')
else:
    DEMO_PARAGRAPH_JSON = os.path.join(settings.BASE_DIR, 'data/demo/reverse_resume_private.json')


ONLY_DONE_INPUT_DIRECTORIES = ['data/data_for_updates/dev_input_step_one/done',
                               'data/data_for_updates/dev_input_step_three/done',
                               'data/data_for_creates/loaded'
                               ]
NOT_DONE_INPUT_DIRECTORIES = ['data/data_for_updates/dev_input_step_one',
                              'data/data_for_updates/dev_input_step_three',
                              'data/data_for_creates']
USED_INPUT_FINAL_DIRECTORY = '/Users/liz/Documents/app_data/archived_input'
