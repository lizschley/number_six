''' Derived from an abstract class containing common functionality for basic paragraph display '''
import constants.sql_substrings as sql_sub
from common_classes.para_link_helper import ParaLinkHelper
from common_classes.para_db_methods import ParaDbMethods
from common_classes.para_display_retriever_base import ParaDisplayRetrieverBase
from helpers.no_import_common_class.paragraph_dictionaries import ParagraphDictionaries
from projects.models.paragraphs import (Group, Paragraph)


VALID_SQL_TYPES = ('group_id_only', 'subtitle')


class ParaDisplayRetrieverDb(ParaDisplayRetrieverBase):
    ''' The ParaDisplayRetrieverDb class retrieves the information to use to output paragraphs.  Later
        there may be other flavors, such as a blog or flash cards'''

    def __init__(self):
        super().__init__()
        # from super
        # for processing db retrieval, not needed for demo (JSON to display)
        # self.ordered = False
        # # for output
        # self.group = {}
        # self.references = []
        # self.paragraphs = []
        # self.para_id_to_link_text = {}
        # self.slug_to_lookup_link = {'para_slug_to_short_title': {},
        #                             'ref_slug_to_short_text': {},
        #                             'group_slug_to_short_name': {}, }
        # from this __init__, all processing variables
        self.para_slugs = []
        self.group_slugs = []
        self.para_ids = []
        self.ref_ids = []

    def data_retrieval(self, kwargs):
        '''
        data_retrieval is to retrieve data from the database when the paragraphs are
        being displayed in the standard way.

        :param kwargs: currently just group_id
        :type kwargs: dict
        :return: a dictionary in the format that works with the standard ParagraphsToDB
        :rtype: dict
        '''
        if 'group_id' in kwargs.keys():
            query = self.write_group_para_sql()
            raw_queryset = ParaDbMethods.class_based_rawsql_retrieval(query, Group, kwargs['group_id'])
            return self.db_output_to_display_input(raw_queryset)

        query = self.write_one_standalone_para_sql()
        raw_queryset = ParaDbMethods.class_based_rawsql_retrieval(query, Paragraph, kwargs['slug'])
        return self.db_output_to_display_input(raw_queryset)

    def write_group_para_sql(self):
        '''
        write_group_para_sql generates the SQL used to retrieve data when it is retrieved
        using a group.
        :return: the query to be used, minus the actual group_id
        :rtype: str
        '''
        query = self.build_basic_sql('group_id_only')
        query += 'where g.id = %s'
        return query

    def write_one_standalone_para_sql(self):
        '''
        write_one_standalone_para_sql generates the SQL used to retrieve data when it is retrieved
        using a paragraph_id

        :return: the query to be used, minus the actual para_id
        :rtype: str
        '''
        query = self.build_basic_sql('single_para')
        query += 'where slug = lower(%s)'
        query += ' and p.standalone = TRUE'
        return query

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
        sql = sql_sub.BEGIN_SELECT
        if sql_type == 'group_id_only':
            sql += ', ' + sql_sub.SELECT_GROUP
        sql += ', ' + sql_sub.SELECT_PARAGRAPHS + ', ' + sql_sub.SELECT_REFERENCES + ' '
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
            sql += sql_sub.FROM_GROUP_JOIN_PARA + ' '
        else:
            sql += sql_sub.FROM_PARA + ' '
        sql += sql_sub.JOIN_REFERENCES_TO_PARA
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
        self.create_lookup_for_paragraph_links()
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
            if row.link_text is not None:
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
            self.ordered = not row.group_type == 'standalone'
            self.group = {
                'group_title': row.group_title,
                'group_note': row.group_note,
                'group_type': row.group_type,
            }
        except AttributeError:  # Be explicit with catching exceptions.
            self.ordered = False
            self.group = {
                'group_title': 'standalone para',
                'group_note': '',
                'group_type': '',
            }

    def append_unique_reference(self, row):
        '''
        append_unique_reference ensuring that even if a reference is used in multiple
        paragraphs, the process to create the link is only done once

        :param row: queryset row, not normalized!
        :type row: one row of django.db.models.query.RawQuerySet
        '''
        if row.reference_id not in self.ref_ids:
            ref = ParagraphDictionaries.reference_link_data(row)
            self.references.append(ref)
            self.ref_ids.append(row.reference_id)
            self.slug_to_lookup_link['ref_slug_to_short_text'][ref['slug']] = ref['short_text']

    def append_unique_paragraph(self, row):
        '''
        append_unique_paragraph ensures that even if a paragraph is repeated that it is only
        processed one time.

        :param row: queryset row, not normalized!
        :type row: one row of django.db.models.query.RawQuerySet
        '''
        if row.paragraph_id not in self.para_ids:
            para = self.paragraph_dictionary(row)
            self.unique_slug_lists(para['text'])
            self.paragraphs.append(para)
            self.para_ids.append(row.paragraph_id)

    def create_lookup_for_paragraph_links(self):
        '''
        create_lookup_for_paragraph_links creates a lookup dictionary with the lookup key, which is
        always a slug, though can be for a reference, paragraph or a group

        Note - making updating true (__init__ for ParaDbMethods), so that an exception will be raised if
        the slug doesn't get a record

        :param para_text: para_text to be searched for the slugs to create the internal links
        :type para: str
        '''
        para_getter = ParaDbMethods(True)
        for para_slug in self.para_slugs:
            link_para = para_getter.find_record(Paragraph, {'slug': para_slug})
            self.slug_to_lookup_link['para_slug_to_short_title'][link_para.slug] = link_para.short_title

    def unique_slug_lists(self, para_text):
        '''
        unique_slug_lists extracts the slugs from the paragraph using the link indicators, thus
        ensuring that the resulting array of slugs used for lookup is unique

        :param para_text: text from one paragraph that is being retrieved
        :type para: str
        :return: list of slugs used for looking up data needed for internal links
        :rtype: list of strings
        '''
        replacing_text = False
        link_helper = ParaLinkHelper(replacing_text)
        data = link_helper.links_from_indicators(para_text, {})
        self.para_slugs = data['para_slugs']
        self.group_slugs = data['group_slugs']

    def paragraph_dictionary(self, row):
        '''
        paragraph_dictionary is one formatted paragraph to be added to a paragraph list.  This
        dict must be in format expected by ParagraphsForDisplay

        :param row: queryset row
        :type row: one row of django.db.models.query.RawQuerySet
        :return: dictionary for one paragraph formatted in a way that works for ParagraphsForDisplay
        :rtype: dict
        '''
        order = 0
        try:
            order = row.order
        except AttributeError:  # Be explicit with catching exceptions.
            print('No row.order, expected when para is only one')
        return {
            'id': row.paragraph_id,
            'subtitle': row.subtitle,
            'note': row.subtitle_note,
            'text': row.text,
            'image_path': row.image_path,
            'image_info_key': row.image_info_key,
            'slug': row.para_slug,
            'short_title': row.short_title,
            'order': self.get_paragraph_order(row.subtitle, order),
        }
