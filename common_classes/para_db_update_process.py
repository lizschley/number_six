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

ASSOCIATION_KEYS = ('add_paragraph_reference', 'add_group_paragraph', 'delete_paragraph_reference',
                    'delete_group_paragraph')

CREATE_RECORD_KEYS = ('add_categories', 'add_groups', 'add_references')

CREATE_DATA = {
    'add_categories': {'unique_field': 'title', 'class': Category, },
    'add_references': {'unique_field': 'link_text', 'class': Reference, },
    'add_groups': {'unique_field': 'title', 'class': Group, },
}

UPDATE_DATA = {
    'categories': {'unique_field': 'slug', 'class': Category},
    'references': {'unique_field': 'slug', 'class': Reference},
    'paragraphs': {'unique_field': 'guid', 'class': Paragraph},
    'groups': {'unique_field': 'slug', 'class': Group},
    'paragraph_reference': {'unique_field': 'id', 'class': ParagraphReference},
    'group_paragraph': {'unique_field': 'id', 'class': GroupParagraph}
}

ASSOCIATION_DATA = {
    'paragraph_reference': {'paragraph_id': 'paragraph_guid', 'reference_id': 'reference_slug'},
    'group_paragraph': {'group_id': 'group_slug', 'reference_id': 'paragraph_guid'},
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
        self.process_data = {'categories': [],
                             'groups': [],
                             'references': [],
                             'paragraphs': []}

    def process_input_data_update_db(self):
        # print(f'self.input_data=={self.input_data}')
        # print(f'self.updating=={self.updating}')
        self.create_record_loop()
        self.update_record_loop()
        self.add_associations()
        self.delete_associations()
        print(f'self.process_data=={self.process_data}')

    def create_record_loop(self):
        for key in CREATE_RECORD_KEYS:
            if utils.key_not_in_dictionary(self.input_data['file_data'], key):
                continue
            for record in self.input_data['file_data'][key]:
                self.find_or_create_wrapper(key, record)

    def update_record_loop(self):
        for key in RECORD_KEYS:
            if utils.key_not_in_dictionary(self.input_data['file_data'], key):
                continue
            for record in self.input_data['file_data'][key]:
                self.find_and_update_wrapper(key, record)

    def find_or_create_wrapper(self, key, record):
        unique_field = CREATE_DATA[key]['unique_field']
        class_ = CREATE_DATA[key]['class']
        find_dict = {unique_field: record[unique_field]}
        create_dict = self.add_category_to_group(record) if key == 'add_groups' else record
        returned_record = self.find_or_create_record(class_, find_dict, create_dict)
        record_dict = self.ensure_dictionary(class_, returned_record)
        self.assign_to_process_data(key, record_dict, unique_field)
        print(f'{returned_record.__class__.__name__} found_or_created: {returned_record}')

    def ensure_dictionary(self, class_, record):
        if record.__class__.__name__ == class_.__name__:
            return record.__dict__
        return record

    def assign_to_process_data(self, key, record, unique_field):
        temp = key.split('_')
        top_process_key = temp[1]
        record_key = record[unique_field]
        self.process_data[top_process_key].append({record_key: record})

    def find_and_update_wrapper(self, key, record):
        unique_field = UPDATE_DATA[key]['unique_field']
        class_ = UPDATE_DATA[key]['class']
        find_dict = {unique_field: record[unique_field]}
        returned_record = self.find_and_update_record(class_, find_dict, record)
        if utils.key_in_dictionary(returned_record, 'error'):
            sys.exit(returned_record['error'])
        print(f'{returned_record.__class__.__name__} updated: {returned_record}')

    def add_category_to_group(self, group_to_create):
        cat_title = group_to_create.pop('category_title', '')
        if not cat_title:
            return self.pop_cat_id_if_zero(group_to_create)
        cat_list = self.process_data['categories']
        if not cat_list:
            return self.pop_cat_id_if_zero(group_to_create)
        cat = utils.find_value_from_dictionary_list(cat_list, cat_title)
        if self.updating:
            group_to_create['category_id'] = cat[0]['id']
        else:
            group_to_create['category_id'] = 99
        return group_to_create

    def pop_cat_id_if_zero(self, group_to_create):
        if group_to_create['category_id'] == 0:
            group_to_create.pop('category_id', None)
        return group_to_create

    def add_associations(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'add_associations'):
            return
        print(self.input_data)

    def delete_associations(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'delete_associations'):
            return
        print(self.input_data)
