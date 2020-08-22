'''These are the input to the batch json db updater process.  In development the update
   itself is manual, but in production we will update based on updated_at

    Rule: this format is not used to create new groups, references or paragraphs
    in development.  Use normal create for that.  Do use if to create categories, though

    *** Question - will the autoslug and auto guid be a problem?  May have to change the model.
'''
import os
import portfolio.settings as settings
from projects.models.paragraphs import Category


BLOG = Category.CATEGORY_TYPE_CHOICES[0][0]
RESUME = Category.CATEGORY_TYPE_CHOICES[1][0]
FLASH_CARD = Category.CATEGORY_TYPE_CHOICES[2][0]


INPUT_TO_DEV_UPDATER = {
    'para_ids': [],
    'add_categories': [{'title': 'Reverse Chronological Resume', 'type': RESUME},
                       {'title': 'Functional Resume', 'type': RESUME}],
    'add_groups': [{'title': 'QA Automation', 'note': '', 'category_id': None,
                    'category_title': 'Functional Resume'}, ],
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
