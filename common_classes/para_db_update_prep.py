''' ParaDbUpdatePrep - further documentation:
        usage: scripts/db_updater_1
        detailed: scripts/documentation/update_process.md'''
# pylint: pylint: disable=unused-import
import sys

import constants.crud as crud
import constants.scripts as constants
import constants.sql_substrings as sql_substrings
import utilities.date_time as dt
import utilities.json_methods as json_helper
import utilities.random_methods as utils
from helpers.no_import_common_class.paragraph_dictionaries import ParagraphDictionaries as para_dict
from projects.models.paragraphs import (Category, Group,  # noqa: F401
                                        GroupParagraph, Paragraph,
                                        ParagraphReference, Reference)
from common_classes.para_db_methods import ParaDbMethods


class ParaDbUpdatePrep(ParaDbMethods):
    '''
        The ParaDbUpdatePrep class retrieves the existing data and relationships used to update
        paragraphs.
    '''

    def __init__(self, input_data, updating=False):
        '''
            Based on the input data, we collect information to be edited in order to update the
            database.  These variables will eventually be written to JSON to be manually updated
            and used as input to the update process
        '''
        # https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
        # this is the output data
        super().__init__(updating)
        self.for_prod = input_data.pop('for_prod', False)
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
            which is created manually and passed in by scripts/db_updater_s1 (some input can only
            be passed in as parameters. See documentation in script)

            Step 1 will never be run in production, since data is updated only in development
        '''
        self.process_input_and_output()

        params = {}
        params['directory_path'] = self.input_data['output_directory']
        params['prefix'] = constants.PROD_PROCESS_IND if self.for_prod else constants.DEFAULT_PREFIX
        json_helper.write_dictionary_to_file(self.output_data, **params)

    def process_input_and_output(self):
        '''
            process_input_and_output is the process where we prepare the data to be updated.

            1. Validate the keys to limit careless mistakes.

            2. Retrieve the existing data, so that we know what to update.
                * Note - The whole prep can be eliminated if there are only only the add_* or delete_*
                         keys

            3. Copy any input that does not depend on data retrieval.  These keys are in
            crud.COPY_DIRECTLY_TO_OUTPUT
        '''
        self.validate_input_keys()
        if self.for_prod:
            self.unique_key_lookup_to_output()
        self.retrieve_existing_data()
        self.copy_directly_to_output()

    def validate_input_keys(self):
        '''
            validate_input_keys ensures that the user is doing careful work and does not make a careless
            mistake by running tests on the input keys.

            If there is an error, then processing stops with a message indicating the necessary
            correction
        '''
        if self.invalid_keys():
            sys.exit((f'Input error: there is at least one invalid key: {self.file_data}; '
                      f'The valid keys are {crud.VALID_RETRIEVAL_KEYS + crud.COPY_DIRECTLY_TO_OUTPUT}'))
        if self.for_prod_with_adds():
            sys.exit(f'Input error: no explicit creates if for_prod: {self.file_data}')
        if not self.valid_input_keys():
            sys.exit(f'Input error: Must be at least one valid key: {self.file_data}')

    def copy_directly_to_output(self):
        '''
            Copy_directly_to_output is a convenience feature to make it so the user can itemize all the
            work needed in step 1.  This prepatory process step retrieves data for updates and must be
            run beforehand (to capture the existing data and relationships), but the input can also have
            some add_* or delete_* keys, which are not prepared for or implemented until step 3.

            For COPY_DIRECTLY_TO_OUTPUT data, you can prepare the input and it will carry over to the
            next step by copying it directly to the manual json file.
        '''
        for key in crud.COPY_DIRECTLY_TO_OUTPUT:
            if utils.key_not_in_dictionary(self.file_data, key):
                continue
            self.output_data[key] = self.file_data[key]

    def retrieve_existing_data(self):
        '''
            retrieve_existing_data is necessary for updating records.  It builds the query according to
            the input critera, retrieves the records from the database, creates a dictionary with the
            information and then writes the dictionary to the output directory as a JSON file.

            After any manual updates (step 2), the file becomes input to the db_update_s3 process.
        '''
        for key in crud.VALID_RETRIEVAL_KEYS:
            if utils.key_not_in_dictionary(self.file_data, key):
                continue
            query = self.build_sql(key)
            if query is None:
                continue
            # print(f'Retrieval query == {query}')
            raw_queryset = ParaDbMethods.class_based_rawsql_retrieval(query, Paragraph)
            self.add_existing_data_to_output(raw_queryset)

    # Validation routines
    def invalid_keys(self):
        '''
            invalid_keys tests if there are any invalid keys, exiting with error message if there are

            :return: True if there are invalid keys and False otherwise
            :rtype: bool
        '''
        for key in self.file_data.keys():
            if key not in crud.VALID_RETRIEVAL_KEYS + crud.COPY_DIRECTLY_TO_OUTPUT:
                return True
        return False

    def for_prod_with_adds(self):
        '''
            for_prod_with_adds validates that when we are using the for_prod input indicator we are
            not doing explicit creates on associations, categories, groups or references

            :return: returns True when for_prod is True and the are input keys like add_*
            :rtype: bool
        '''
        if not self.for_prod:
            return False
        return utils.dictionary_key_begins_with_substring(self.file_data, 'add_')

    def valid_input_keys(self):
        '''
            valid_input_keys ensures that there is at least one key

            :return: True if there is at least one valid key, False otherwise
            :rtype: bool
        '''
        num = 0
        for key in crud.VALID_RETRIEVAL_KEYS + crud.COPY_DIRECTLY_TO_OUTPUT:
            if utils.key_in_dictionary(self.file_data, key):
                num += 1
        return num > 0

    # retrieval routines
    def build_sql(self, key):
        '''
            build_sql uses the JSON input file to build a where statement.  It appends the where
            to the rest of the sql from the complete query

            :return: complete sql query with where that varies depending on input file
            :rtype: str
        '''
        where = self.get_where_statement(key)
        if where is None:
            print(f'No where for key=={key}, therefore not editing existing records{self.file_data}')
            return None
        query = ParaDbUpdatePrep.complete_query_from_constants()
        query += where + ' order by c.id, g.cat_sort, gp.order'
        return query

    @staticmethod
    def complete_query_from_constants():
        '''
            complete_query_from_constants creates complete paragraph query other than where statement

            :return: Query for paragraphs
            :rtype: str
        '''
        query = sql_substrings.BEGIN_SELECT + ', ' + sql_substrings.COMPLETE_CATEGORY_SELECT + ', '
        query += sql_substrings.COMPLETE_GP_SELECT + ', ' + sql_substrings.COMPLETE_GROUP_SELECT + ', '
        query += sql_substrings.COMPLETE_PR_SELECT + ', ' + sql_substrings.COMPLETE_PARAGRAPH_SELECT
        query += ', ' + sql_substrings.COMPLETE_REFERENCE_SELECT
        query += sql_substrings.FROM_PARA + sql_substrings.JOIN_GROUP_TO_PARA
        query += sql_substrings.JOIN_CATEGORY_TO_GROUP + sql_substrings.JOIN_REFERENCES_TO_PARA
        return query

    def get_where_statement(self, key):
        '''
            get_where_statement creates a where statement based on the contents of the input JSON file

            :return: where clause
            :rtype: str
        '''
        if key in ('group_ids', 'category_ids', 'paragraph_ids', 'reference_ids'):
            return 'where ' + key[0] + '.id in (' + self.get_where_ids(key) + ')'
        if key == 'updated_at':
            return self.get_updated_at_where()

        return None

    def get_updated_at_where(self):
        '''
            get_updated_at_where creates a where statement that uses the updated_at field to retrieve
            recently updated paragraph information

            :return: a where statement based on updated_at input (dict from file_data) parameters
            :rtype: str
        '''
        info = self.file_data['updated_at']
        oper = info['oper']
        units = info['units']
        use_date = f"'{dt.timediff_from_now_for_where(oper, units)}'"
        return self.upated_at_loop_through_tables(use_date)

    @staticmethod
    def upated_at_loop_through_tables(use_date):
        '''
            upated_at_loop_through_tables writes a where to pull in all of the updated paragraph data

            :param use_date: date in a format that works with postgres timestamps with time zones
            :type use_date: str
            :return: where statement using the use_date to get the records updated after that timestamp
            :rtype: str
        '''
        logical_op = ''
        where = 'where'
        for ind in crud.TABLE_ABBREV:
            where += f' {logical_op} {ind}.updated_at >= {use_date}'
            logical_op = 'or'
        return where

    def get_where_ids(self, key):
        '''
            get_where_ids takes an array of ids and turns it a string to be used as part of a where
            statement.  The key will be one of these: 'group_ids', 'category_ids', 'paragraph_ids'
            or 'reference_ids'

            This saves the user some effort, by allowing ints to be passed in.  Otherwise, if the user
            did not add quotes, the code would throw a ValueError

            :param key: key to a python list of ids
            :type key: str (will do the conversion)
            :return: string with ids in the format to be used in sql, such as g.id in (1, 2, 3)
            :rtype: str
        '''
        return ', '.join(map(str, self.file_data[key]))

    def add_existing_data_to_output(self, queryset):
        '''
            add_existing_data_to_output takes each row and assigns it to a dictionary representation of
            the database record.  If it was already assigned, it will return without doing anything.

            The resulting list of dictionaries will be used to find and update or, if you are using the
            output in production, to find or create.

            :param queryset: result from the database retrieval using the input file parameters
            :type queryset: raw queryset
        '''
        for row in queryset:
            self.assign_category(row)
            self.assign_reference(row)
            self.assign_paragraph(row)
            self.assign_group(row)
            self.assign_groupparagraph(row)
            self.assign_paragraphreference(row)

    def assign_category(self, row):
        '''
            assign_category takes category data, does a lookup and if it has not been output yet, creates
            a dictionary representation of the database record.

            :param row: queryset row
            :type row: queryset row
        '''
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
        if self.for_prod:
            self.for_prod_lookup('categories', row.category_id, row.category_slug)

    def for_prod_lookup(self, top_key, key, value):
        '''
            for_prod_lookup will be used in production or in testing that production will work.
            It creates a way to lookup the production record by associating the development id with the
            unique_keys that are the same in all environments and primary keys (ids)
            which will probably differ between environments.  This allows us keep associations between
            records in sync.

            :param top_key: valid top keys are in <UPDATE_RECORD_KEYS> (import constants.crud as crud)
            :type top_key: str
            :param key: str version of the primary id for the given record
            :type key: int
            :param value: unique key that is different from the primary key
            :type value: str
        '''
        try:
            str_key = str(key)
        except ValueError:
            sys.exit(f'can not convert key to string {key}')

        self.output_data['record_lookups'][top_key][str_key] = value
        self.output_data['record_lookups'][top_key][value] = {'dev_id': key}

    def assign_reference(self, row):
        '''
            assign_reference takes reference data, does a lookup and if it has not been output yet,
            creates a dictionary representation of the database record.

            :param row: queryset row
            :type row: queryset row
        '''
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
        ref['short_text'] = row.short_text
        self.output_data['references'].append(ref)
        if self.for_prod:
            self.for_prod_lookup('references', row.reference_id, row.reference_slug)

    def assign_paragraph(self, row):
        '''
            assign_paragraph takes paragraph data, does a lookup and if it has not been output yet,
            creates a dictionary representation of the database record.

            :param row: queryset row
            :type row: queryset row
        '''
        if row.para_id is None:
            return
        if row.para_id in self.included_ids['paragraphs']:
            return
        self.included_ids['paragraphs'].append(row.para_id)
        para = para_dict.paragraph_dictionary()
        para['id'] = row.para_id
        para['subtitle'] = row.para_subtitle
        para['short_title'] = row.short_title
        para['note'] = row.para_note
        para['text'] = row.para_text
        para['standalone'] = row.para_standalone
        para['image_path'] = row.para_image_path
        para['image_info_key'] = row.para_image_info_key
        para['guid'] = row.para_guid
        para['slug'] = row.para_slug
        self.output_data['paragraphs'].append(para)
        if self.for_prod:
            self.for_prod_lookup('paragraphs', row.para_id, row.para_guid)

    def assign_group(self, row):
        '''
            assign_group takes group data, does a lookup and if it has not been output yet, creates
            a dictionary representation of the database record.

            :param row: queryset row
            :type row: queryset row
        '''
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
        group['short_name'] = row.group_short_name
        group['cat_sort'] = row.cat_sort
        group['group_type'] = row.group_type
        self.output_data['groups'].append(group)
        if self.for_prod:
            self.for_prod_lookup('groups', row.group_id, row.group_slug)
            self.record_lookups('categories', row.group_category_id, Category)

    def assign_groupparagraph(self, row):
        '''
            assign_groupparagraph takes groupparagraph data, does a lookup and creates a dictionary
            representation of the database record, if it does not already exist.

            :param row: queryset row
            :type row: queryset row
        '''
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
        if self.for_prod:
            self.record_lookups('groups', row.gp_group_id, Group)
            self.record_lookups('paragraphs', row.gp_para_id, Paragraph)

    def assign_paragraphreference(self, row):
        '''
            assign_paragraphreference takes paragraphreference data, does a lookup and creates a
            dictionary representation of the database record, unless one already exists.

            :param row: queryset row
            :type row: queryset row
        '''
        if row.pr_id is None:
            return
        if row.pr_id in self.included_ids['paragraph_reference']:
            return
        self.included_ids['paragraph_reference'].append(row.pr_id)
        para_ref = para_dict.paragraphreference_dictionary()
        para_ref['id'] = row.pr_id
        para_ref['reference_id'] = row.pr_reference_id
        para_ref['paragraph_id'] = row.pr_para_id
        self.output_data['paragraph_reference'].append(para_ref)
        if self.for_prod:
            self.record_lookups('references', row.pr_reference_id, Reference)
            self.record_lookups('paragraphs', row.pr_para_id, Paragraph)

    def record_lookups(self, top_key, pk_id, class_):
        '''
            record_lookups will make sure that there is a way to uniquely identify records
            that may have a different primary key in production

            :param top_key: top key to lookup table: plural form of the main four paragraph records
            :type top_key: str
            :param pk_id: key for lookup: primary key of the record we need to look up
            :type pk_id: int
            :param class_: models.Model class for the lookup
            :type class_: models.Model
        '''
        if top_key == 'categories' and pk_id is None:
            return
        dict_to_check = self.output_data['record_lookups'][top_key]
        if utils.key_not_in_dictionary(dict_to_check, pk_id):
            rec = class_.objects.get(pk=pk_id)
            if top_key == 'paragraphs':
                self.for_prod_lookup(top_key, rec.id, rec.guid)
                return
            self.for_prod_lookup(top_key, rec.id, rec.slug)

    def unique_key_lookup_to_output(self):
        '''
            unique_key_lookup_to_output is the dictionary framework used to associate the development
            primary keys that may differ between environments to the unique keys that will be the same
            in all environments.  This ensures that the development associations make it up to
            production.

            Development is the source of truth.

            :return: the structure of the lookup table, with only the top keys
            :rtype: dict
        '''
        self.output_data['record_lookups'] = {
            'categories': {},
            'references': {},
            'paragraphs': {},
            'groups': {},
        }
