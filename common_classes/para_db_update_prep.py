''' DbUpdateParagraphRetriever, class used for retrieving the data for batch updates '''
import json
import sys

import constants.scripts as constants
import constants.sql_substrings as sql_substrings
from common_classes.para_db_methods import ParaDbMethods
from common_classes.paragraph_db_input_creator import ParagraphDbInputCreator
from projects.models.paragraphs import (Category, Group, GroupParagraph,
                                        Paragraph, ParagraphReference,
                                        Reference)
from utilities.paragraph_dictionaries import ParagraphDictionaries as para_dict

BLOG = Category.CATEGORY_TYPE_CHOICES[0][0]
RESUME = Category.CATEGORY_TYPE_CHOICES[1][0]
FLASH_CARD = Category.CATEGORY_TYPE_CHOICES[2][0]

VALID_RETRIVAL_KEYS = ('updated_at', 'group_ids', 'category_ids', 'paragraph_ids')
VALID_INPUT_KEYS = ('updated_at', 'group_ids', 'category_ids', 'paragraph_ids', 'add_categories',
                    'add_references', 'add_groups', 'delete_associations', 'add_associations')
VALID_CREATE_KEYS = ('add_categories', 'add_references', 'add_groups')
VALID_ASSOCIATION_KEYS = ('delete_associations', 'add_associations')


class ParaDbUpdatePrep(ParaDbMethods):
    ''' The ParaDbUpdatePrep class retrieves the information used to update paragraphs.
        It should ONLY be instantiated by scripts.batch_json_db_updater unless the process
        changes.  It is designed to run in both development and production.  See comments in
        scripts.batch_json_db_updater for more information '''

    def __init__(self, input_data, updating=False):
        ''' Based on the input data, we collect information to be edited in order to update the
            database.  These variables will eventually be written to JSON to be manually updated
        '''
        # https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
        # this is the output data
        super(ParaDbUpdatePrep, self).__init__(updating)
        self.input_data = input_data
        self.included_ids = {
            'categories': [],
            'references': [],
            'paragraphs': [],
            'groups': [],
            'group_paragraph': [],
            'paragraph_reference': [],
        }
        self.output_data = {
            'categories': [],
            'references': [],
            'paragraphs': [],
            'groups': [],
            'group_paragraph': [],
            'paragraph_reference': [],
            'delete_associations': [],
            'add_associations': [],
        }

    def collect_data_and_write_json(self):
        '''
        collect_data_and_write_json is Step 1 of the update process.  It reads the input file,
        which is created manually and passed in by scripts.batch_json_db_updater

        This class should only be instantiated by scripts.batch_json_db_updater, which then moves the
        input file to the done directory and calls the next file, if there is another unprocessed file

        See scripts.batch_json_db_updater for a greater understanding of the entire process

        Step 1 will never be run in production, since data is updated only in development
        '''

        self.process_input_and_output()
        out_dir = self.input_data['output_directory']
        prefix = constants.PROD_PROCESS_IND if self.running_as_prod() else constants.DEFAULT_PREFIX

        output_file = open(ParagraphDbInputCreator.create_json_file_path(directory_path=out_dir,
                                                                         prefix=prefix), 'w')
        # magic happens here to make it pretty-printed
        output_file.write(json.dumps(self.output_data, indent=4, sort_keys=True))
        output_file.close()

    def process_input_and_output(self):
        ''' process_input_and_output is the driver to gather and process data from database'''
        # 1. validate input (only updated_at and ab2b-8bf1f660ae48 else OR one of list of ids)
        # 2. Do creates, add records to output data
        # 3. Retrieve data, add records to output data
        # 4. Add associations to output data
        # 5. write output json

        # right now I am starting with retrive data, since I don't have any creates or associations
        # Todo: do exit.sys('error message') in validate_input and make sure that processing stops and
        # the error is printed for now, will revisit later
        self.validate_input_keys()
        self.create_new_records()
        self.retrieve_existing_data()
        self.prepare_associations()

        # print(f'self.updating=={self.updating}')
        # print(f'self.para_ids == {self.input_data["file_data"]["paragraph_ids"]}')
        # print(f'self.output_data == {self.output_data}')

    def running_as_prod(self):
        return self.input_data['file_data'].get('updated_at', 'ab2b-8bf1f660ae48') != 'ab2b-8bf1f660ae48'

    def validate_input_keys(self):
        ''' '''
        if self.invalid_keys():
            sys.exit(f'Input error: there is at least one invalid key: {self.input_data["file_data"]}')
        if not self.one_or_zero_retrieval_keys():
            sys.exit(f'Input error: too many retrieval keys: {self.input_data["file_data"]}')
        if not self.updated_at_none_or_only():
            sys.exit(f'Input error: updated_at should be the only key: {self.input_data["file_data"]}')
        if not self.valid_input_keys():
            sys.exit(f'Input error: there must be at least one valid key: {self.input_data["file_data"]}')

    def create_new_records(self):
        ''' '''
        for key in VALID_CREATE_KEYS:
            if self.input_data['file_data'].get(key, 'ab2b-8bf1f660ae48') == 'ab2b-8bf1f660ae48':
                continue
            if key == 'add_categories':
                self.add_categories()
            if key == 'add_references':
                self.add_references()
            if key == 'add_groups':
                self.add_groups()

    def retrieve_existing_data(self):
        query = self.build_sql()
        # print(f'Retrieval query == {query}')
        raw_queryset = ParaDbMethods.class_based_rawsql_retrieval(query, Paragraph)
        return self.add_existing_data_to_manual_json(raw_queryset)

    # if we are doing a updated_at retrieval, then we need to get the unique keys for the given
    # associations.  Otherwise there is a possibility for data that cannot be accessed
    # Not really true if it is actually development, but it would be better to do it
    # consistantly
    def prepare_associations(self):
        print('still have not decided exactly how to deal with assoociations')
        for key in VALID_ASSOCIATION_KEYS:
            if self.input_data['file_data'].get(key, 'ab2b-8bf1f660ae48') == 'ab2b-8bf1f660ae48':
                continue
            if key == 'delete_associations':
                self.remove_associations()
            if key == 'delete_associations':
                self.add_associations()

    # Validation routines
    def invalid_keys(self):
        for key in self.input_data['file_data'].keys():
            if key not in VALID_INPUT_KEYS:
                return True
        return False

    def one_or_zero_retrieval_keys(self):
        num = 0
        for key in VALID_RETRIVAL_KEYS:
            if not self.input_data['file_data'].get(key, 'ab2b-8bf1f660ae48') == 'ab2b-8bf1f660ae48':
                num += 1
        return num < 2

    def updated_at_none_or_only(self):
        '''
        updated_at_none_or_only validates that updated_at is only key, if it is an input key

        :return: returns False unless updated_at is not a key or if it is the only key
        :rtype: bool
        '''
        if not self.running_as_prod():
            return True

        if len(self.input_data['file_data'].keys()) >= 1:
            return False
        return False

    def valid_input_keys(self):
        num = 0
        for key in VALID_INPUT_KEYS:
            if not self.input_data['file_data'].get(key, 'ab2b-8bf1f660ae48') == 'ab2b-8bf1f660ae48':
                num += 1
        return num > 0

    # create routines

    # call self.find_or_create_record(self, class_, find_dict, create_dict)
    # these are loops
    def add_categories(self):
        print('dev error: add categories should not be called yet')

    # call self.find_or_create_record(self, class_, find_dict, create_dict)
    # these are loops
    def add_references(self):
        print('dev error: add references should not be called yet')

    # call self.find_or_create_record(self, class_, find_dict, create_dict)
    # these are loops
    def add_groups(self):
        print('dev error: add groups should not be called yet')

    # retrieval routines
    def build_sql(self):
        where = self.get_where_statement()
        if where is None:
            print(f'Not editing existing records {self.input_data["file_data"]}')
            return
        return ParaDbUpdatePrep.complete_query_from_constants() + ' ' + where

    @staticmethod
    def complete_query_from_constants():
        query = sql_substrings.BEGIN_SELECT + ', ' + sql_substrings.COMPLETE_CATEGORY_SELECT + ', '
        query += sql_substrings.COMPLETE_GP_SELECT + ', ' + sql_substrings.COMPLETE_GROUP_SELECT + ', '
        query += sql_substrings.COMPLETE_PR_SELECT + ', ' + sql_substrings.COMPLETE_PARAGRAPH_SELECT
        query += ', ' + sql_substrings.COMPLETE_REFERENCE_SELECT
        query += sql_substrings.FROM_PARA + sql_substrings.JOIN_GROUP_TO_PARA
        query += sql_substrings.JOIN_CATEGORY_TO_GROUP + sql_substrings.JOIN_REFERENCES_TO_PARA
        return query

    def get_where_statement(self):
        for key in VALID_RETRIVAL_KEYS:
            if self.input_data['file_data'].get(key, 'ab2b-8bf1f660ae48') == 'ab2b-8bf1f660ae48':
                continue
            if key in ('group_ids', 'category_ids', 'paragraph_ids'):
                return 'where ' + key[0] + '.id in (' + self.get_where_ids(key) + ')'
            if key == 'updated_at':
                print(f'Have not implemented run_as_prod {self.input_data["file_data"]}')
        return None

    def get_where_ids(self, key):
        return ', '.join(self.input_data['file_data'][key])

    def add_existing_data_to_manual_json(self, queryset):
        for row in queryset:
            self.assign_category(row)
            self.assign_reference(row)
            self.assign_paragraph(row)
            self.assign_group(row)
            self.assign_groupparagraph(row)
            self.assign_paragraphreference(row)

    def assign_category(self, row):
        if row.category_id is None:
            return
        if row.category_id in self.included_ids['categories']:
            return
        self.included_ids['categories'].append(row.category_id)
        category = para_dict.category_dictionary()
        # Todo: field assignment
        self.output_data['categories'].append(category)

    def assign_reference(self, row):
        if row.reference_id is None:
            return
        if row.reference_id in self.included_ids['references']:
            return
        self.included_ids['references'].append(row.reference_id)
        ref = para_dict.reference_dictionary()
        ref['id'] = row.reference_id
        ref['link_text'] = row.reference_link_text
        ref['slug'] = row.reference_slug
        ref['url'] = row.reference_url
        self.output_data['references'].append(ref)

    def assign_paragraph(self, row):
        if row.para_id is None:
            return
        if row.para_id in self.included_ids['paragraphs']:
            return
        self.included_ids['paragraphs'].append(row.para_id)
        para = para_dict.paragraph_dictionary()
        para['id'] = row.para_id
        para['subtitle'] = row.para_subtitle
        para['note'] = row.para_note
        para['text'] = row.para_text
        para['standalone'] = row.para_standalone
        para['image_path'] = row.para_image_path
        para['image_info_key'] = row.para_image_info_key
        para['guid'] = row.para_guid
        self.output_data['paragraphs'].append(para)

    def assign_group(self, row):
        if row.group_id is None:
            return
        if row.group_id in self.included_ids['groups']:
            return
        self.included_ids['groups'].append(row.group_id)
        group = para_dict.group_dictionary()
        group['id'] = row.group_id
        group['title'] = row.group_title
        group['slug'] = row.group_slug
        group['note'] = row.group_note
        group['category_id'] = row.group_category_id
        self.output_data['groups'].append(group)

    def assign_groupparagraph(self, row):
        if row.gp_id is None:
            return
        if row.gp_id in self.included_ids['group_paragraph']:
            return
        self.included_ids['group_paragraph'].append(row.gp_id)
        group_para = para_dict.groupparagraph_dictionary()
        group_para['id'] = row.gp_id
        group_para['group_id'] = row.gp_group_id
        group_para['paragraph_id'] = row.gp_para_id
        group_para['order'] = row.gp_order
        self.output_data['group_paragraph'].append(group_para)

    def assign_paragraphreference(self, row):
        if row.pr_id is None:
            return
        if row.pr_id in self.included_ids['paragraph_reference']:
            return
        self.included_ids['group_paragraph'].append(row.pr_id)
        para_ref = para_dict.paragraphreference_dictionary()
        para_ref['id'] = row.pr_id
        para_ref['reference_id'] = row.pr_reference_id
        para_ref['paragraph_id'] = row.pr_para_id
        self.output_data['paragraph_reference'].append(para_ref)

    # add or delete association routines
    def remove_associations(self):
        print('dev error: remove associations should not be called yet')

    def add_associations(self):
        print('dev error: add associations should not be called yet')
