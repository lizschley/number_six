'''
    Use this as a template for the dictionary input to the data retrieval before updates
'''
import os
import portfolio.settings as settings
from projects.models.paragraphs import Category


BLOG = Category.CATEGORY_TYPE_CHOICES[0][0]
RESUME = Category.CATEGORY_TYPE_CHOICES[1][0]
FLASH_CARD = Category.CATEGORY_TYPE_CHOICES[2][0]


INPUT_TO_DEV_UPDATER = {
    # One of the following:
    'updated_at': None,
    'group_ids': [],
    'category_ids': [],
    'para_ids': [],

    # Any or all of the following (see expected formats below, only for convenience):
    'add_categories': [{'title': 'Reverse Chronological Resume', 'type': RESUME},
                       {'title': 'Functional Resume', 'type': RESUME}],
    'add_references': [],
    'add_groups': [{'title': 'QA Automation', 'note': '', 'category_id': None,
                    'category_title': 'Functional Resume'}, ],
    'delete_associations': [],
    'add_associations': [],

    # can override if you want
    'output_directory': os.path.join(settings.BASE_DIR, 'data/data_for_updates/dev_manual_json/'),
}

# the following is only for convenience, so I can cut and paste original format and then update
EXPECTED_FORMATS = {
    'add_categories': [{'title': '', 'type': ''},
                       {'title': 'Functional Resume', 'type': ''}],
    'add_references': [{'link_text': '', 'url': ''}],
    'add_groups': [{'title': '', 'note': '', 'category_id': None, 'category_title': ''},
                   {'title': 'Functional Resume', 'type': ''}],
    'delete_associations': [{'ref_para': {'para_id': 0, 'ref_id': 0, 'guid': '', 'link_text': ''}},
                            {'group_para': {'para_id': 0, 'group_id': 0, 'guid': '', 'slug': ''}}],
    'add_associations': [{'ref_para': {'para_id': 0, 'ref_id': 0, 'guid': '', 'link_text': ''}},
                         {'group_para': {'para_id': 0, 'group_id': 0, 'guid': '', 'slug': ''}}],
}
