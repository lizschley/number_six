''' DbUpdateParagraphRetriever, class used for retrieving the data for batch updates '''
import json
import constants.common as constants
from common_classes.paragraph_record_crud import ParagraphRecordCrud
from projects.models.paragraphs import (Category, Reference, Paragraph, Group, GroupParagraph,
                                        ParagraphReference)

BLOG = Category.CATEGORY_TYPE_CHOICES[0][0]
RESUME = Category.CATEGORY_TYPE_CHOICES[1][0]
FLASH_CARD = Category.CATEGORY_TYPE_CHOICES[2][0]


class DbUpdateRetrieveOrCreate():
    ''' The DbUpdateRetrieveOrCreate class retrieves the information used to update paragraphs.
        It should ONLY be instantiated by scripts.batch_json_db_updater unless the process
        changes.  It is designed to run in both development and production.  See comments in
        scripts.batch_json_db_updater for more information '''

    def __init__(self, input_data):
        ''' Based on the input data, we collect information to be edited in order to update the
            database.  These variables will eventually be written to JSON to be manually updated
        '''
        # https://stackoverflow.com/questions/8653516/python-list-of-dictionaries-search
        self.input_data = input_data
        self.categories = {'created': [], 'retrieved': []}
        self.references = {'created': [], 'retrieved': []}
        self.paragraphs = {'retrieved': []}
        self.groups = {'created': [], 'retrieved': []}
        self.existing_group_paragraph = []
        self.existing_paragraph_reference = []
        self.delete_associations = []
        self.add_associations = []
        # process data
        self.title_to_group_id = {}
        self.title_to_category_id = {}
        self.link_text_to_reference_id = {}

    def collect_data_and_write_json(self):
        '''
        collect_data_and_write_json is Step 1 of the update process.  It reads the input file,
        which is created manually and passed in by scripts.batch_json_db_updater

        This class should only be instantiated by scripts.batch_json_db_updater, which then moves the
        input file to the done directory and calls the next file, if there is another unprocessed file

        See scripts.batch_json_db_updater for a greater understanding of the entire process

        Step 1 will never be run in production, since data is updated only in development
        '''
        output_data = self.retrieve_data_for_updating()
        with open(self.input_data['path_to_json'], 'w') as file_path:
            json.dump(output_data, file_path)

    def retrieve_data_for_updating(self):
        '''
        The most update data_retrieval input paramaters are documented by the template used to create
        the input data. It will be kept up-to-date because it is used to format the input data.
        Here is the path: data/dictionary_templates/starting_dev_process_input.py

        self.input_data will be the input throughout the retrieval process

        :return: a dictionary in the format necessary for updating the database
        :rtype: dict
        '''
        self.input_data = self.initial_updates(self.input_data)
        self.retrieve_existing_data()
        return self.dictionary_for_update()

    def retrieve_existing_data(self):
        pass

    def dictionary_for_update(self):
        '''
        dictionary_for_update is the dictionary to be written to the output JSON for editing

        :return: dictionary used in the format used by the database updater (not yet created)
        :rtype: dict
        '''
        return {
            'categories':  self.categories,
            'references': self.references,
            'paragraphs': self.paragraphs,
            'groups': self.groups,
            'existing_group_paragraph': self.existing_group_paragraph,
            'existing_paragraph_reference': self.existing_paragraph_reference,
            'add_associations': self.add_associations,
            'delete_associations': self.delete_associations,
        }

# begin example ideas only (from another class)

    def build_basic_sql(self, sql_type):
        '''
        basic_sql creates the sql code to retrieve paragraphs and their related records

        :return: sql with the necessary elements and without where statements
        :rtype: str
        '''
        return self.get_tables(self.get_select(sql_type), sql_type)

    def get_select(self, sql_type):
        '''
        get_select builds the select for the given sql type (depends on how paragraphs are used)
        Sql type is set based key word args

        :param sql_type: Select part of query will be different based on value.
        :type sql_type: str
        :return: select part of the sql query
        :rtype: str
        '''
        sql = constants.BEGIN_SELECT
        if sql_type == 'group_id_only':
            sql += ', ' + constants.SELECT_GROUP
        sql += ', ' + constants.SELECT_PARAGRAPHS + ', ' + constants.SELECT_REFERENCES + ' '
        return sql

    def get_tables(self, sql, sql_type):
        '''
        get_tables builds the tables and joins for the given sql type (depends on how paragraphs are
        used) Sql type is set based key word args

        :param sql: the sql query built so far
        :type sql: str
        :param sql_type: Tables part of query will be different based on value.
        :type sql_type: str
        :return: Partial query
        :rtype: str
        '''
        if sql_type == 'group_id_only':
            sql += constants.FROM_GROUP_JOIN_PARA + ' '
        else:
            sql += constants.FROM_PARA + ' '
        sql += constants.JOIN_REFERENCES_TO_PARA
        return sql

    def db_output_to_display_input(self, raw_queryset):
        '''
        db_output_to_display_input returns the exactly formatted data used by the standard
        ParagraphsToDB to create the formatted dictionary to be used in the template

        :param raw_queryset: data returned after running the query
        :type raw_queryset: django.db.models.query.RawQuerySet instance
        :return: dictionary used by the basic display paragraph template
        :rtype: dict
        '''
        self.loop_through_queryset(raw_queryset)
        return self.output_data()

    def loop_through_queryset(self, query_set):
        '''
        loop_through_queryset to format data in the way needed by ParagraphsForDisplay

        :param query_set: All the paragraphs that were retrieved in queryset form
        :type query_set: django.db.models.query.RawQuerySet instance
        '''
        for row in query_set:
            if not self.group:
                self.first_row_assignments(row)
            self.add_ref_to_paragraph_link_txt_dictionary(row.paragraph_id, row.link_text)
            self.append_unique_reference(row)
            self.append_unique_paragraph(row)

    # Todo: eventually validate that if one row.order is zero in set, they all are
    def first_row_assignments(self, row):
        '''
        first_row_assignments makes up for the fact that querysets are not normalized by
        ensuring that data we expect to be in every row is only processed in the first
        row

        :param row: All the data needed for a given paragraph, plus some repeated data
        :type row: queryset row
        '''
        try:
            self.ordered = row.order != 0
            self.group = {
                'title': row.title,
                'note': row.note,
            }
        except AttributeError: # Be explicit with catching exceptions.
            self.ordered = False
            self.group = {
                'title': 'standalone para',
                'note': '',
            }

    def append_unique_reference(self, row):
        '''
        append_unique_reference ensuring that even if a reference is used in multiple
        paragraphs, the process to create the link is only done once

        :param row: queryset row, not normalized!
        :type row: one row of django.db.models.query.RawQuerySet
        '''
        if row.reference_id not in self.ref_ids:
            self.references.append({'link_text': row.link_text, 'url': row.url})
            self.ref_ids.append(row.reference_id)

    def append_unique_paragraph(self, row):
        '''
        append_unique_paragraph ensures that even if a paragraph is repeated that it is only
        processed one time.

        :param row: queryset row, not normalized!
        :type row: one row of django.db.models.query.RawQuerySet
        '''
        if row.paragraph_id not in self.para_ids:
            self.paragraphs.append(self.paragraph_dictionary(row))
            self.para_ids.append(row.paragraph_id)
