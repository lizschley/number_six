'''Constants used in testing'''
# pylint: disable=missing-function-docstring
import os

import portfolio.settings as settings

BASIC_PARA_DICT_KEY = 'basic_paragraph_input_dict/value'
BASIC_PARA_TEST_JSON = os.path.join(settings.BASE_DIR, 'testing/data/basic_paragraph.json')

DISPLAY_PARA_DICT_KEY = 'basic_paragraph_display_dict/value'
DISPLAY_PARA_DB_DICT_KEY = 'basic_paragraph_db_display_dict/value'

DISPLAY_PARA_KEYS = ['group_type', 'paragraphs', 'title', 'title_note']
