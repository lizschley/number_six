''' This is Step Three of the database update process.  Step 1 retrieves & Step 2 edits the data '''
# pylint: pylint: disable=unused-import

import sys
import helpers.no_import_common_class.utilities as utils

from common_classes.para_db_methods import ParaDbMethods
from projects.models.paragraphs import (Category, Group,  # noqa: F401
                                        GroupParagraph, Paragraph,
                                        ParagraphReference, Reference)

RECORD_KEYS = ('categories', 'references', 'paragraphs', 'groups',
               'paragraph_reference', 'group_paragraph')

ASSOCIATION_KEYS = ('add_associations', 'delete_associations')

ASSOCIATION_RECORD_KEYS = ('paragraph_reference', 'group_paragraph')

UPDATE_DATA = {
    'categories': {'unique_field': 'slug', 'class': Category},
    'references': {'unique_field': 'slug', 'class': Reference},
    'paragraphs': {'unique_field': 'guid', 'class': Paragraph},
    'groups': {'unique_field': 'slug', 'class': Group},
    'paragraph_reference': {'unique_field': 'id', 'class': ParagraphReference},
    'group_paragraph': {'unique_field': 'id', 'class': GroupParagraph}
}


class ParaDbUpdateProcess(ParaDbMethods):
    '''
        ParaDbUpdateProcess updates (or if production or run_as_prod, creates) data based on
        self.input_data
    '''

    def __init__(self, input_data, updating):
        '''
        __init__ Assign the framework needed to ...
        '''
        super(ParaDbUpdateProcess, self).__init__(updating)
        self.input_data = input_data

    def process_input_data_update_db(self):
        # print(f'self.input_data=={self.input_data}')
        # print(f'self.updating=={self.updating}')
        self.update_record_loop()
        self.add_associations()
        self.delete_associations()

    def update_record_loop(self):
        for key in RECORD_KEYS:
            if utils.key_not_in_dictionary(self.input_data['file_data'], key):
                continue
            for record in self.input_data['file_data'][key]:
                self.find_and_update_wrapper(key, record)

    def find_and_update_wrapper(self, key, record):
        unique_field = UPDATE_DATA[key]['unique_field']
        class_ = UPDATE_DATA[key]['class']
        find_dict = {unique_field: record[unique_field]}
        returned_record = self.find_and_update_record(class_, find_dict, record)
        if utils.key_in_dictionary(returned_record, 'error'):
            sys.exit(returned_record['error'])
        print(f'{returned_record.__class__.__name__} updated: {returned_record}')

    def add_associations(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'add_associations'):
            return

    def delete_associations(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'delete_associations'):
            return
