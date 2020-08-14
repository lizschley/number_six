'''These are the input to the batch json db updater process.  In development the update
   itself is manual, but in production we will update based on updated_at

    Rule: this format is not used to create new groups, references or paragraphs
    in development.  Use normal create for that.  Do use if to create categories, though

    *** Question - will the autoslug and auto guid be a problem?  May have to change the model.
'''
import os
import portfolio.settings as settings

INPUT_TO_DEV_UPDATER = {
    'updated_at': None,
    'group_ids': [],
    'new_categories': [{'title': 'Reverse Chronological Resume', 'type': 'resume'}],
    'category_ids': [],
    'para_ids': [],
    'subtitle': [],
    'guid': [],
    'delete_associations': [],
    'add_associations': [],
    'output_directory': os.path.join(settings.BASE_DIR, 'data/update_json/dev_input/original_data/'),
}

UPDATER_FILE_INPUT = {
    'is_prod': False,
    'categories': [],
    'groups': [],
    'references': [],
    'paragraphs': [],
    'associations': {
        'delete': [
            {
                'group_category': [{'group': '', 'category': ''}, ],
                'group_paragraph': [{'group': '', 'para': ''}, ],
                'paragraph_reference': [{'para': '', 'ref': ''}, ],
            },
        ],
        'add': [
            {
                'group_category': [{'group': '', 'category': ''}, ],
                'group_paragraph': [{'group': '', 'para': ''}, ],
                'paragraph_reference': [{'para': '', 'ref': ''}, ],
            },
        ],
    },
    'cat_id_to_title': {},
    'group_id_to_title': {},
    'ref_id_to_link_text': {},
    'para_id_to_guid': {},
}
