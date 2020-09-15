''' DbUpdateParagraphRetriever, class used for retrieving the data for batch updates '''
# pylint: pylint: disable=unused-import
import json
import sys

import constants.scripts as constants
import constants.sql_substrings as sql_substrings
from common_classes.para_db_methods import ParaDbMethods
from common_classes.paragraph_db_input_creator import ParagraphDbInputCreator
import helpers.no_import_common_class.date_time as dt
import helpers.no_import_common_class.utilities as utils
from projects.models.paragraphs import (Category, Group, GroupParagraph,  # noqa: F401
                                        Paragraph, ParagraphReference,
                                        Reference)
from utilities.paragraph_dictionaries import ParagraphDictionaries as para_dict


VALID_RETRIEVAL_KEYS = ('updated_at', 'group_ids', 'category_ids', 'paragraph_ids')
COPY_DIRECTLY_TO_OUTPUT = ('add_categories', 'add_references', 'add_groups', 'add_paragraph_reference',
                           'add_group_paragraph', 'delete_paragraph_reference', 'delete_group_paragraph')
TABLE_ABBREV = ('c', 'g', 'p', 'r', 'gp', 'pr')


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
        self.run_as_prod = input_data.pop('run_as_prod', False)
        self.file_data = input_data.pop('file_data')
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
        prefix = constants.PROD_PROCESS_IND if self.run_as_prod else constants.DEFAULT_PREFIX

        output_file = open(ParagraphDbInputCreator.create_json_file_path(directory_path=out_dir,
                                                                         prefix=prefix), 'w')
        # magic happens here to make it pretty-printed
        output_file.write(json.dumps(self.output_data, indent=4, sort_keys=True))
        output_file.close()

    def process_input_and_output(self):
        ''' process_input_and_output is the driver to gather and process data from database'''
        # 1. validate input (only updated_at OR one of list of ids)
        # 2. Do creates, add records to output data
        # 3. Retrieve data, add records to output data
        # 4. Add associations to output data
        # 5. write output json

        # right now I am starting with retrive data, since I don't have any creates or associations
        # Todo: do exit.sys('error message') in validate_input and make sure that processing stops and
        # the error is printed for now, will revisit later
        self.validate_input_keys()
        self.retrieve_existing_data()
        self.copy_directly_to_output()

    def validate_input_keys(self):
        '''
        validate_input_keys ensures that the user (me) is doing careful work

        It runs some tests on the input keys and errors with a message, if the tests fail
        '''
        if self.invalid_keys():
            sys.exit((f'Input error: there is at least one invalid key: {self.file_data}; '
                      f'The valid keys are {VALID_RETRIEVAL_KEYS + COPY_DIRECTLY_TO_OUTPUT}'))
        if not self.one_or_zero_retrieval_keys():
            sys.exit(f'Input error: too many retrieval keys: {self.file_data}')
        if self.run_as_prod_with_adds():
            sys.exit(f'Input error: no explicit creates if run_as_prod: {self.file_data}')
        if not self.valid_input_keys():
            sys.exit(f'Input error: Must be at least one valid key: {self.file_data}')

    def copy_directly_to_output(self):
        '''
        copy_directly_to_output is a convenience feature, so you can think about what you want to do
        upfront.  This class does not do any database creates, updates or deletes, but by retrieving the
        paragraph structure in record format, it makes it easy to edit for updating.
        '''
        for key in COPY_DIRECTLY_TO_OUTPUT:
            if utils.key_not_in_dictionary(self.file_data, key):
                continue
            self.output_data[key] = self.file_data[key]

    def retrieve_existing_data(self):
        '''
        retrieve_existing_data [summary]

        [extended_summary]

        :return: [description]
        :rtype: [type]
        '''
        query = self.build_sql()
        # print(query)
        if query is None:
            return None
        # print(f'Retrieval query == {query}')
        raw_queryset = ParaDbMethods.class_based_rawsql_retrieval(query, Paragraph)
        return self.add_existing_data_to_manual_json(raw_queryset)

    # Validation routines
    def invalid_keys(self):
        for key in self.file_data.keys():
            if key not in VALID_RETRIEVAL_KEYS + COPY_DIRECTLY_TO_OUTPUT:
                return True
        return False

    def one_or_zero_retrieval_keys(self):
        num = 0
        for key in VALID_RETRIEVAL_KEYS:
            if not utils.key_not_in_dictionary(self.file_data, key):
                num += 1
        return num < 2

    def run_as_prod_with_adds(self):
        '''
        run_as_prod_with_adds validates that when we are using the run_as_prod input indicator we are
        not doing explicit creates on associations, categories, groups or references

        :return: returns True when run_as_prod is True and the are input keys like add_*
        :rtype: bool
        '''
        if not self.run_as_prod:
            return False
        return utils.dictionary_key_begins_with_substring(self.file_data, 'add_')

    def valid_input_keys(self):
        num = 0
        for key in VALID_RETRIEVAL_KEYS + COPY_DIRECTLY_TO_OUTPUT:
            if not utils.key_not_in_dictionary(self.file_data, key):
                num += 1
        return num > 0

    # retrieval routines
    def build_sql(self):
        where = self.get_where_statement()
        if where is None:
            print(f'Not editing existing records {self.file_data}')
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
        for key in VALID_RETRIEVAL_KEYS:
            if utils.key_not_in_dictionary(self.file_data, key):
                continue
            if key in ('group_ids', 'category_ids', 'paragraph_ids'):
                return 'where ' + key[0] + '.id in (' + self.get_where_ids(key) + ')'
            if key == 'updated_at':
                return self.get_updated_at_where()

        return None

    def get_updated_at_where(self):
        info = self.file_data['updated_at']
        oper = info['oper']
        units = info['units']
        use_date = f"'{dt.timediff_from_now_for_where(oper, units)}'"
        return self.upated_at_loop_through_tables(use_date)

    def upated_at_loop_through_tables(self, use_date):
        logical_op = ''
        where = 'where'
        for ind in TABLE_ABBREV:
            where += f' {logical_op} {ind}.updated_at > {use_date}'
            logical_op = 'or'
        return where

    def get_where_ids(self, key):
        return ', '.join(self.file_data[key])

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
        category['id'] = row.category_id
        category['title'] = row.category_title
        category['slug'] = row.category_slug
        category['category_type'] = row.category_type
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
