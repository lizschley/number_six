'''Constants used in testing'''
# pylint: disable=missing-function-docstring
import os

import portfolio.settings as settings

BASIC_PARA_DICT_KEY = 'basic_paragraph_input_dict/value'
BASIC_PARA_TEST_JSON = os.path.join(settings.BASE_DIR, 'testing/data/basic_paragraph.json')

DISPLAY_PARA_DICT_KEY = 'basic_paragraph_display_dict/value'
DB_DISPLAY_PARA_INPUT_FILENAME = 'testing/data/db_data_para_input_pickle.pkl'
DB_DISPLAY_PARA_INPUT_PICKLE = os.path.join(settings.BASE_DIR, DB_DISPLAY_PARA_INPUT_FILENAME)

DISPLAY_PARA_KEYS = ['paragraphs', 'title', 'title_note']
