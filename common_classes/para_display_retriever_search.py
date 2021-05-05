''' Derived from an abstract class containing common functionality for basic paragraph display '''
import constants.sql_substrings as sql_sub
from projects.models.paragraphs import Group  # noqa: F401
from common_classes.para_db_methods import ParaDbMethods
from common_classes.para_display_retriever_db import ParaDisplayRetrieverDb
from helpers.no_import_common_class.paragraph_dictionaries import ParagraphDictionaries


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
        self.search_term = ''
        self.group_ids = []
        self.first_row = True
        self.counter = 0

    def data_retrieval(self, kwargs):
        '''
        data_retrieval is to retrieve data from the database when the paragraphs associated with a group
        are displayed together based on the paragraph order.

        :param kwargs: currently just search_id
        :type kwargs: dict
        :return: a dictionary in the format that works with the standard ParagraphsForDisplayCat
        :rtype: dict
        '''
        like_term = kwargs['search_term'].strip()
        self.search_term = like_term
        like_term = '%' + like_term + '%'
        query = self.build_search_sql()
        raw_queryset = ParaDbMethods.class_based_rawsql_retrieval(query, Group, like_term,
                                                                  like_term, like_term)
        if len(raw_queryset) == 0:
            self.assign_no_results_group()
            return self.output_data()
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

    @staticmethod
    def search_where():
        '''
        search_where constructs where statement

        :param kwargs: information to specify field and value for where
        :type kwargs: dict
        :return: where statement with variable and its value
        :rtype: dict
        '''
        not_in = ('archived', 'resume')
        no_search = 'no_search'

        where = (f"where c.category_type not in {not_in} and group_type <> '{no_search}' and (g.title "
                 f"like %s or p.subtitle like %s or p.text like %s) ")
        return where

    def basic_search_sql(self):
        '''
        basic_search_sql creates the sql code to retrieve multiple groups associated with a given
        search.  It will also return associated paragraphs and their related records

        :return: sql with the necessary elements and without where statements
        :rtype: str
        '''
        beg_sql = sql_sub.BEGIN_SELECT + ', ' + sql_sub.SELECT_SEARCH + ' '
        sql_tables = sql_sub.FROM_GROUP_JOIN_PARA + sql_sub.JOIN_CATEGORY_TO_GROUP
        return beg_sql + sql_tables

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
            'group_title': f'Search results for term: {self.search_term}',
            'group_note': '',
            'group_type': 'ordered',
        }

    def append_unique_paragraph(self, row):
        '''
        append_unique_paragraph creates paragraph records for display that only have links to data
        records. There are three types of links:  Two links are for paragraph records that are
        standalone: to a popup and to a single paragraph page.  The third link is to a page that displays
        ordered paragraphs that all belong to a given group

        :param row: queryset row, not normalized!
        :type row: one row of django.db.models.query.RawQuerySet
        '''
        beg_para_text = '<p>'
        end_para_text = '</p>'
        para_text = ''

        if ((row.para_id not in self.para_ids) and (len(row.para_slug) > 1) and row.standalone):
            self.para_ids.append(row.para_id)
            self.para_slugs.append(row.para_slug)
            para_text += beg_para_text + f'|beg|{row.para_slug}|end|; '
            para_text += f'|beg_para|{row.para_slug}|end_para|' + end_para_text

        if row.group_id not in self.group_ids and row.group_type == 'ordered':
            self.group_ids.append(row.group_id)
            self.group_slugs.append(row.group_slug)
            para_text += beg_para_text + '<strong>Ordered Paragraphs:</strong> '
            para_text += f'|beg_group|{row.group_slug}|end_group|' + end_para_text

        if para_text:
            self.counter += 1
            new_para = ParagraphDictionaries.paragraph_dictionary()
            new_para['text'] = para_text
            new_para['order'] = self.counter
            self.paragraphs.append(new_para)

    def assign_no_results_group(self):
        ''' error group '''
        self.group = {
            'group_title': f'No search results for term: {self.search_term}',
            'group_note': '',
            'group_type': 'error',
        }
