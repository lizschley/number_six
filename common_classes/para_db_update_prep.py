''' DbUpdateParagraphRetriever, class used for retrieving the data for batch updates '''
import json
import sys
import constants.scripts as constants
import constants.sql_substrings as sql_substrings
from common_classes.para_db_methods import ParaDbMethods
from common_classes.paragraph_db_input_creator import ParagraphDbInputCreator
from projects.models.paragraphs import (Category, Reference, Paragraph, Group, GroupParagraph,
                                        ParagraphReference)

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
            'existing_group_paragraph': [],
            'existing_paragraph_reference': [],
        }
        self.output_data = {
            'categories': [],
            'references': [],
            'paragraphs': [],
            'groups': [],
            'existing_group_paragraph': [],
            'existing_paragraph_reference': [],
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
        self.add_and_delete_associations()

        # print(f'self.updating=={self.updating}')
        # print(f'self.para_ids == {self.input_data["file_data"]["paragraph_ids"]}')
        # print(f'self.output_data == {self.output_data}')

    def running_as_prod(self):
        return self.input_data['file_data'].get('updated_at', 'ab2b-8bf1f660ae48') != 'ab2b-8bf1f660ae48'

    def validate_input_keys(self):
        ''' '''
        print('inside validate_input_keys')
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
        print('in create_new records')
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
        print('in retrieve existing data')
        query = self.build_sql()

    # if we are doing a updated_at retrieval, then we need to get the unique keys for the given
    # associations.  Otherwise there is a possibility for data that cannot be accessed
    # Not really true if it is actually development, but it would be better to do it
    # consistantly
    def add_and_delete_associations(self):
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
        return ParaDbUpdatePrep.query_from_complete_constants() + ' ' + where

    @staticmethod
    def query_from_complete_constants():
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

    # add or delete association routines
    def remove_associations(self):
        print('dev error: remove associations should not be called yet')

    def add_associations(self):
        print('dev error: add associations should not be called yet')

#         self.create_standalone_records()
#         self.retrieve_and_process_update_input()


#     def create_standalone_records(self):
#         pass

#     def retrieve_and_process_update_input(self):
#         pass






# # begin example ideas only (from another class)


#     def build_complete_retrieve_sql(self, sql_type):
#         '''
#         basic_sql creates the sql code to retrieve paragraphs and their related records

#         :return: sql with the necessary elements and without where statements
#         :rtype: str
#         '''
#         return self.get_tables(self.get_select(sql_type), sql_type)

#     def get_select(self, sql_type):
#         '''
#         get_select builds the select for the given sql type (depends on how paragraphs are used)
#         Sql type is set based key word args

#         :param sql_type: Select part of query will be different based on value.
#         :type sql_type: str
#         :return: select part of the sql query
#         :rtype: str
#         '''
#         sql = sql_substrings.BEGIN_SELECT
#         sql += ', ' + sql_substrings.SELECT_PARAGRAPHS + ', ' + sql_substrings.SELECT_REFERENCES + ' '
#         return sql

#     def get_tables(self, sql, get_category=False):
#         '''
#         get_tables builds the tables and joins for the given sql type (depends on how paragraphs are
#         used) Sql type is set based key word args

#         :param sql: the sql query built so far
#         :type sql: str
#         :param sql_type: Tables part of query will be different based on value.
#         :type sql_type: str
#         :return: Partial query
#         :rtype: str
#         '''
#         sql += sql_substrings.FROM_PARA + ' '
#         sql += sql_substrings.JOIN_REFERENCES_TO_PARA
#         sql += sql_substrings.JOIN_GROUP_TO_PARA
#         sql += sql_substrings.JOIN_CATEGORY_TO_GROUP
#         return sql

#     def db_output_to_display_input(self, raw_queryset):
#         '''
#         db_output_to_display_input returns the exactly formatted data used by the standard
#         ParagraphsToDB to create the formatted dictionary to be used in the template

#         :param raw_queryset: data returned after running the query
#         :type raw_queryset: django.db.models.query.RawQuerySet instance
#         :return: dictionary used by the basic display paragraph template
#         :rtype: dict
#         '''
#         self.loop_through_queryset(raw_queryset)
#         return self.output_data()

#     def loop_through_queryset(self, query_set):
#         '''
#         loop_through_queryset to format data in the way needed by ParagraphsForDisplay

#         :param query_set: All the paragraphs that were retrieved in queryset form
#         :type query_set: django.db.models.query.RawQuerySet instance
#         '''
#         existing_ids = { 'group': [], 'category': [], 'reference': []}
#         for row in query_set:
#             print(f'row=={row}, {existing_ids}')


#     # Todo: eventually validate that if one row.order is zero in set, they all are
#     def first_row_assignments(self, row):
#         '''
#         first_row_assignments makes up for the fact that querysets are not normalized by
#         ensuring that data we expect to be in every row is only processed in the first
#         row

#         :param row: All the data needed for a given paragraph, plus some repeated data
#         :type row: queryset row
#         '''
#         try:
#             self.ordered = row.order != 0
#             self.group = {
#                 'title': row.title,
#                 'note': row.note,
#             }
#         except AttributeError: # Be explicit with catching exceptions.
#             self.ordered = False
#             self.group = {
#                 'title': 'standalone para',
#                 'note': '',
#             }

#     def append_unique_reference(self, row):
#         '''
#         append_unique_reference ensuring that even if a reference is used in multiple
#         paragraphs, the process to create the link is only done once

#         :param row: queryset row, not normalized!
#         :type row: one row of django.db.models.query.RawQuerySet
#         '''
#         if row.reference_id not in self.ref_ids:
#             self.references.append({'link_text': row.link_text, 'url': row.url})
#             self.ref_ids.append(row.reference_id)

#     def append_unique_paragraph(self, row):
#         '''
#         append_unique_paragraph ensures that even if a paragraph is repeated that it is only
#         processed one time.

#         :param row: queryset row, not normalized!
#         :type row: one row of django.db.models.query.RawQuerySet
#         '''
#         if row.paragraph_id not in self.para_ids:
#             self.paragraphs.append(self.paragraph_dictionary(row))
#             self.para_ids.append(row.paragraph_id)
