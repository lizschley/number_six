''' This is Step Three of the database update process.  Step 1 retrieves & Step 2 edits the data '''
# pylint: pylint: disable=unused-import

import sys
import helpers.no_import_common_class.utilities as utils

from common_classes.para_db_methods import ParaDbMethods
from projects.models.paragraphs import (Category, Group,  # noqa: F401
                                        GroupParagraph, Paragraph,
                                        ParagraphReference, Reference)

FILE_DATA = 'file_data'

UPDATE_RECORD_KEYS = ('categories', 'references', 'paragraphs', 'groups',
                      'paragraph_reference', 'group_paragraph')

ASSOCIATION_KEYS = ('add_paragraphreference', 'add_groupparagraph',
                    'delete_paragraphreference', 'delete_groupparagraph')

CREATE_RECORD_KEYS = ('add_categories', 'add_groups', 'add_references')

CREATE_DATA = {
    'add_categories': {'unique_fields': ['title'], 'class': Category, },
    'add_references': {'unique_fields': ['link_text'], 'class': Reference, },
    'add_groups': {'unique_fields': ['title'], 'class': Group, },
    'add_paragraphs': {'unique_fields': ['guid'], 'class': Paragraph, },
    'add_groupparagraph': {'unique_fields': ['group_id', 'paragraph_id'],
                           'class': GroupParagraph, },
    'add_paragraphreference': {'unique_fields': ['paragraph_id', 'reference_id'],
                               'class': ParagraphReference, }
}

DELETE_ASSOCIATIONS = {
    'delete_groupparagraph': {'class': GroupParagraph, },
    'delete_paragraphreference': {'class': ParagraphReference, }
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
    'paragraphreference': {'paragraph': {'unique_fields': ['guid'], 'class': Paragraph},
                           'reference': {'unique_fields': ['slug'], 'class': Reference}, },
    'groupparagraph': {'group': {'unique_fields': ['slug'], 'class': Group},
                       'paragraph': {'unique_fields': ['guid'], 'class': Paragraph}, },
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
        self.file_data = input_data.pop('file_data')
        self.input_data = input_data
        # print(f'input_data == {self.input_data}')
        self.process_data = {'categories': [],
                             'groups': [],
                             'references': [],
                             'paragraphs': [],
                             'associations_to_create': [],
                             'associations_to_delete': [], }

    def process_input_data_update_db(self):
        self.validate_input_keys()
        self.create_record_loop(CREATE_RECORD_KEYS, self.file_data)
        self.update_record_loop()
        self.add_or_delete_associations()
        # print(f'self.process_data=={self.process_data}')

    def validate_input_keys(self):
        '''
        validate_input_keys ensures that the user (me) is doing careful work

        It runs some tests on the input keys and errors with a message, if the tests fail
        '''
        if self.explicit_creates_in_prod():
            sys.exit(f'Input error: no explicit creates if production or run_as_prod: {self.file_data}')

    def explicit_creates_in_prod(self):
        '''
        explicit_creates_in_prod validates both in production or when we are mimicing the production
        process, we will never allow explicit creates.  All creates will be as if the data was first
        created in development and will now be created in production with the same unique keys (other
        than the id, which may or may not be the same)

        :return: returns True when it's a production run and there are input keys like add_*
        :rtype: bool
        '''
        if not self.input_data['is_prod'] and not self.input_data['run_as_prod']:
            return False
        return utils.dictionary_key_begins_with_substring(self.file_data, 'add_')

    def create_record_loop(self, keys, input_data):
        for key in keys:
            if utils.key_not_in_dictionary(self.file_data, key):
                continue
            for record in input_data[key]:
                self.find_or_create_wrapper(key, record)

    def update_record_loop(self):
        for key in UPDATE_RECORD_KEYS:
            if utils.key_not_in_dictionary(self.file_data, key):
                continue
            for record in self.file_data[key]:
                self.find_and_update_wrapper(key, record)

    def find_or_create_wrapper(self, key, record):
        unique_fields = CREATE_DATA[key]['unique_fields']
        class_ = CREATE_DATA[key]['class']
        find_dict = {}
        for field in unique_fields:
            # print(f'in for, field == {field}, record == {record}')
            find_dict[field] = record[field]
        create_dict = self.add_category_to_group(record) if key == 'add_groups' else record
        returned_record = self.find_or_create_record(class_, find_dict, create_dict)
        record_dict = self.ensure_dictionary(class_, returned_record)
        if len(unique_fields) == 1:
            self.assign_to_process_data(key, record_dict, unique_fields[0])
        print(f'{returned_record.__class__.__name__} found_or_created: {returned_record}')

    def ensure_dictionary(self, class_, record):
        if record.__class__.__name__ == class_.__name__:
            return record.__dict__
        return record

    def assign_to_process_data(self, key, record, unique_field):
        info = utils.dict_from_split_string(key, '_', ('nothing', 'top_key'))
        record_key = record[unique_field]
        self.process_data[info['top_key']].append({record_key: record})

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

    def add_or_delete_associations(self):
        '''
        add_or_delete_associations starts the process of reading data from the add and delete
        associations portion of the input data.  This will be used when you want to associate a
        paragraph with another group, for example.  Usually adding a reference will be done in a
        normal update, but if you just forgot to add a reference, this is an easy fix.

        This is called only in Step 3 since it involves changing data in the database

        Throughout much of this process we have constants that drive the input data, directing to
        the correct process
        '''
        for input_key in ASSOCIATION_KEYS:
            if utils.key_not_in_dictionary(self.file_data, input_key):
                continue
            info = utils.dict_from_split_string(input_key, '_', ('function', 'data_key'))

            input_dictionaries = self.prepare_association_data(self.file_data[input_key],
                                                               info['data_key'])
            if info['function'] == 'delete':
                self.delete_associations(input_key, input_dictionaries)
            elif info['function'] == 'add':
                self.add_associations(input_key, input_dictionaries)

    def add_associations(self, input_key, create_dict_list):
        print(f'create_dict_list: {create_dict_list}')
        for create_dict in create_dict_list:
            self.find_or_create_wrapper(input_key, create_dict)

    def delete_associations(self, input_key, find_dict_list):
        class_to_delete = DELETE_ASSOCIATIONS[input_key]['class']
        for find_dict in find_dict_list:
            self.delete_record(class_to_delete, find_dict)

    def prepare_association_data(self, file_input_list, data_key):
        '''
        prepare_association_data takes the file input (which is a list) from the input file:
           data/data_for_updates/dev_input_step_three directory

        It also uses data from constants at the top of this file:
           ASSOCIATION_KEY
           ASSOCIATION_DATA
           CREATE_DATA

        The final result is a find or create on the association create dictionary

        :param input_key: key from input json: found in data/data_for_updates/dev_input_step_three
        :type input_key: str
        :param data_key: last part of the input_key is the key to ASSOCIATION_DATA constant
        :type data_key: str
        '''
        input_dictionaries = []
        for file_input in file_input_list:
            input_dictionaries.append(self.dict_from_foreign_associations(file_input, data_key))
        return input_dictionaries

    def dict_from_foreign_associations(self, foreign_key_records, data_key):
        '''
        dict_from_foreign_associations reads the input file and finds the two foreign associations
        (input_data), using the following format to find the foreign key records to associate
        groups with paragraphs or paragraphs with references.
        Here are two foreign key input_data examples:
        1.  [{"paragraph_guid": "a3575efb-e443-48da-89d7-20f8c5910229",
              "reference_slug": "unclebobmartincleancodeprogrammerspeakerteacher"}]
        2.  [{"group_slug": "functional-resume",
              "paragraph_guid": "21028615-1e01-4444-acc9-e581637e460b"}]

        Number 1 usage - For the paragraph_reference it finds the Paragraph using the guid and the
                         Reference using the slug.
        Number 2 usage - For the group_paragraph association, if finds the Group from the group slug
                         and the Paragraph from the paragraph guid.

        Once it finds the records, it gets the id to create the return dictionary

        example of return: {'paragraph_id': 9, 'reference_id': 9}

        :param foreign_key_records: dictionary from the input data (from json file mentioned earlier)
        :type foreign_key_records: dict
        :param data_key: key obtained from parsing input_data key.  Used to find ASSOCIATION_DATA
        :type data_key: str
        :return: dictionary that is used to create or delete the new association record
        :rtype: dict
        '''
        association_data = ASSOCIATION_DATA[data_key]
        create_dict = {}
        for rec in foreign_key_records:
            association_key = self.current_association_key(rec)
            input_dict = {rec: foreign_key_records[rec]}
            data = association_data[association_key]
            create_dict.update(self.one_create_key_and_value(input_dict, association_key, data))
        return create_dict

    def one_create_key_and_value(self, input_dict, association_key, association_data):
        '''
        one_create_key_and_value takes the input record and the ASSOCIATION_DATA and puts it together
        to find one of the foreign records (Group, Paragraph or Record) so we use the key value pair,
        for example: {'paragraph_id': 9}

        :param input_dict: unique key information to find the foreign key parts of the association record
        :type input_dict: dict
        :param association_key: string
        :type association_key: used to find the necessary information to do the database lookups
        :param association_data: Constants used to understand the associations
        :type association_data: dict
        :return: one key value pair that is part of the data needed to create the association record
        :rtype: dict
        '''
        # input_dict == {'paragraph_guid': 'para_guid_r_a', 'reference_slug': 'ref_slug_a'}
        # or input_dict == {'group_slug': 'group_slug_a', 'paragraph_guid': 'parag_guid_g_a'}
        # association_data[key] = {'unique_fields': ['guid'], 'class': Paragraph} for example
        unique_field_name = association_data['unique_fields'][0]
        input_key = association_key + '_' + unique_field_name
        unique_value = input_dict[input_key]
        record = self.find_record(association_data['class'], {unique_field_name: unique_value})
        create_field_name = association_key + '_id'
        return {create_field_name: record.id}

    def current_association_key(self, association_from_input):
        '''
        current_assoication_key parses the input for the given record.  All we need is the first
        part, since it is the key to the ASSOCIATION_DATA, which is used by both add and delete
        associations to find the class and the unique field to find the object

        :param association_from_input: key to ASSOCIATION_DATA parsed from input data
        :type association_from_input: dict
        :return: the specific key needed in to obtain the data needed
        :rtype: str
        '''
        info = utils.dict_from_split_string(association_from_input, '_', ['association_key'])
        return info['association_key']
