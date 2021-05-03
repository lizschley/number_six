''' Derived from an abstract class containing common functionality for basic paragraph display '''
import constants.sql_substrings as sql_sub
from projects.models.paragraphs import Group  # noqa: F401
from common_classes.para_db_methods import ParaDbMethods
from common_classes.para_display_retriever_db import ParaDisplayRetrieverDb


class ParaDisplayRetrieverSearch(ParaDisplayRetrieverDb):
    ''' The ParaDisplayRetrieverSearch class retrieves the information to use to build paragraphs from
        the search terms.  The paragraphs will be links of the various types:
        ordered groups (flash cards and study), stand_alone paragraphs: Add popup link or link to its
        own page
    '''

    def __init__(self):
        '''
        __init__ different from the base class


        '''
        super().__init__()
        # have already
        # self.ordered
        # self.ref_ids = []
        # self.references = []
        # self.para_slugs = []
        # self.group_slugs = []
        # self.para_ids = []
        # self.ref_ids = []

        # for processing
        self.group_ids = []
        self.first_row = True
        self.search_term = ''

    def data_retrieval(self, kwargs):
        '''
        data_retrieval is to retrieve data from the database when the paragraphs associated with a group
        are displayed together based on the paragraph order.

        :param kwargs: currently just search_id
        :type kwargs: dict
        :return: a dictionary in the format that works with the standard ParagraphsForDisplayCat
        :rtype: dict
        '''
        self.search_term = kwargs['search_term']
        query = self.build_search_sql()
        breakpoint()
        raw_queryset = ParaDbMethods.class_based_rawsql_retrieval(query, Group,)
        return self.db_output_to_display_input(raw_queryset)

    def build_search_sql(self):
        '''
        build_search_sql builds sql that will pull in groups and their paragraphs and references
        for a given search

        :param kwargs: This will have search_term
        :type kwargs: dict
        :return: The data retrieved, everything associated search display
        :rtype: dict
        '''
        query = self.basic_search_sql()
        where = self.search_where()
        query += ' ' + where + ' order by g.group_type, p.subtitle '
        return query

    def search_where(self):
        '''
        search_where constructs where statement

        :param kwargs: information to specify field and value for where
        :type kwargs: dict
        :return: where statement with variable and its value
        :rtype: dict
        '''
        where = "where c.search_type not in (archived', 'resume') and group_type <> 'no_search' " +\
                "and (g.title like '%" + self.search_term + "%' or p.subtitle like '%" +\
                self.search_term + "%' or p.text like '%" + self.search_term + "%'"
        return where

    def basic_search_sql(self):
        '''
        basic_search_sql creates the sql code to retrieve multiple groups associated with a given
        search.  It will also return associated paragraphs and their related records

        :return: sql with the necessary elements and without where statements
        :rtype: str
        '''
        beg_sql = self.get_search_select()
        sql_tables = self.get_search_tables()
        return beg_sql + sql_tables

    def get_search_select(self):
        '''
        get_search_select builds the select for the given sql type (depends on how paragraphs are used)
        Sql type is set based key word args

        :param sql_type: Select part of query will be different based on value.
        :type sql_type: str
        :return: select part of the sql query
        :rtype: str
        '''
        return sql_sub.BEGIN_SELECT + ', ' + sql_sub.SELECT_SEARCH + ' '

    def get_search_tables(self):
        '''
        get_tables builds the tables and joins search sql

        :return: Partial query
        :rtype: str
        '''
        return sql_sub.FROM_GROUP_JOIN_PARA + sql_sub.JOIN_CATEGORY_TO_GROUP

    def loop_through_queryset(self, query_set):
        '''
        loop_through_queryset to format data in the way needed by ParagraphsForDisplay

        :param query_set: All the paragraphs that were retrieved in queryset form
        :type query_set: django.db.models.query.RawQuerySet instance
        '''
        for row in query_set:
            if self.first_row:
                self.first_row = False
                self.first_row_assignments(row)
            self.append_unique_paragraph(row)

    def first_row_assignments(self, row):
        '''
        first_row_assignments creates the pretend group data for outputting search results as if they
        are paragraphs from an ordered group

        :param row: All the data needed for a given paragraph, plus some repeated data
        :type row: queryset row
        '''
        self.ordered = True
        self.group = {
            'title': f'Search Results for Search Term: {self.search_term}',
            'id': 999,
            'group_type': 'ordered',
        }

    def append_unique_paragraph(self, row):
        '''
        append_unique_paragraph ensures that even if a paragraph is in multiple rows, and even if it is
        it used in multiple groups, it will be displayed once and only once for this group

        :param row: queryset row, not normalized!
        :type row: one row of django.db.models.query.RawQuerySet
        '''
        beg_para_text = '<p>'
        end_para_text = '</p>'

        if row.paragraph_id not in self.para_ids:
            self.para_ids.append(row.paragraph_id)
            self.para_slugs.append(row.para_slug)
            new_para = beg_para_text + '<strong>Standalone:</strong> ' f'|beg|{row.para_slug}|end|;'
            new_para += f'|beg_para|{row.para_slug}|end_para|' + end_para_text
            self.paragraphs.append(new_para)

        if row.group_id not in self.group_ids:
            self.group_ids.append(row.group_id)
            self.group_slugs.append(row.group_slug)
            new_para = beg_para_text + '<strong>Ordered:</strong> '
            new_para += f'|beg_group|{row.group_slug}|end_group|' + end_para_text
            self.paragraphs.append(new_para)

    def output_data(self):
        '''
        output_data is different for categories because there are many groups and one search
        The references are associated with the group, in the display
        The groups are ordered and should not be displayed individually

        :return: dictionary used to display groups and paragraphs associated with a given search
        :rtype: dict
        '''
        return {'group': self.group,
                'para_id_to_link_text': self.para_id_to_link_text,
                'slug_to_lookup_link': self.slug_to_lookup_link, }
