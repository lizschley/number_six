'''
    This is a csv to JSON utility to edit and use however is needed

    For example, a way to quickly move paragraphs to and from various groups

    The input is created using sql like:  originals/sql/comma_delim_group_slugs_with_text_guids.sql
    Must be to be modified, but it saves a lot of typing
'''
# pylint: disable=missing-function-docstring
import os
from portfolio.settings import BASE_DIR
import constants.scripts as constants
from helpers.no_import_common_class.paragraph_dictionaries import ParagraphDictionaries
import utilities.json_methods as json_helper
import utilities.random_methods as utils


IN_CSV_FILE = os.path.join(BASE_DIR, 'data/csv/resume_slugs_and_text.csv')
OUT_JSON_PATH = constants.INPUT_TO_UPDATER_STEP_THREE


def run():
    '''
        usage as follows:
        >>> python manage.py runscript -v3 csv_to_json_creator

        Example input data, like so:
        [
            {
                'guid': 'd40b2a7a-21a8-4b58-81b2-1beabba8bd6b',
                'group_slug': 'organization-and-documentation, quality-and-maintenance',
                'add_group': 'dev-ops-and-automation',
                'remove_group': ''
            },
        ]

        Creating data with the following format:
        input_data = {
            'add_group_paragraph': [
                {
                    'group_slug': '',
                    'paragraph_guid': ''
                }
            ],
            'delete_group_paragraph': [
                {
                    'group_slug': '',
                    'paragraph_guid': ''
                }
            ]
        }
    '''
    file_data = {
        'add_group_paragraph': [],
        'delete_group_paragraph': []
    }

    list_data = utils.dictionary_list_from_csv(IN_CSV_FILE)

    for data in list_data:
        add = ParagraphDictionaries.group_para_associations(data['guid'],
                                                            data['add_group'])
        file_data['add_group_paragraph'] += add
        delete = ParagraphDictionaries.group_para_associations(data['guid'],
                                                               data['remove_group'])
        file_data['delete_group_paragraph'] += delete

    params = {'out_json_path': OUT_JSON_PATH}
    json_helper.write_dictionary_to_file(file_data, **params)
