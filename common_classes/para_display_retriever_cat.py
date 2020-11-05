''' Derived from an abstract class containing common functionality for basic paragraph display '''
import constants.sql_substrings as sql_sub
from common_classes.para_db_methods import ParaDbMethods
from common_classes.para_display_retriever_db import ParaDisplayRetrieverDb
from projects.models.paragraphs import Category


VALID_SQL_TYPES = ('category_id')


class ParaDisplayRetrieverCat(ParaDisplayRetrieverDb):
    ''' The ParaDisplayRetrieverCat class retrieves the information to use to output multiple groups
        and their associated paragraphs.  All reference links will be displayed below all of the
        paragraphs associated with a given group.  Hoping that this class will work with all of the
        planned categories.'''

    def __init__(self):
        '''
        __init__ different from the base class

        Groups are the driving force here:
            self.groups = [{'group': group_dict, 'paragraphs': [], 'link_text': []}]
        '''
        super().__init__()
        # have already
        # self.ordered
        # self.ref_ids = []
        # self.references = []

        # for processing
        self.group_ids = []
        self.group_id_to_link_text_list = {}
        self.group_id_to_para_ids = {}
        # for output (also self.references from base class)
        self.category = {}
        self.groups = []

    def data_retrieval(self, kwargs):
        '''
        data_retrieval is to retrieve data from the database when the paragraphs associated with a group
        are displayed together based on the paragraph order.

        :param kwargs: currently just category_id
        :type kwargs: dict
        :return: a dictionary in the format that works with the standard ParagraphsForDisplayCat
        :rtype: dict
        '''
        sql_results = self.build_category_sql(kwargs)
        raw_queryset = ParaDbMethods.class_based_rawsql_retrieval(sql_results['query'], Category,
                                                                  sql_results['param'])
        return self.db_output_to_display_input(raw_queryset)

    def build_category_sql(self, kwargs):
        '''
        build_category_sql builds sql that will pull in groups and their paragraphs and references
        for a given category

        :param kwargs: This will have either a category id or a category slug
        :type kwargs: dict
        :return: The data retrieved, everything associated with the category
        :rtype: dict
        '''
        query = self.basic_category_sql()
        where = self.category_where(kwargs)
        query += ' ' + where['statement'] + ' ' + sql_sub.CATEGORY_SORT
        return {'query': query, 'param': where['param']}

    def category_where(self, kwargs):
        '''
        category_where constructs where statement

        :param kwargs: information to specify field and value for where
        :type kwargs: dict
        :return: where statement with variable and its value
        :rtype: dict
        '''
        where = 'where '
        if 'category_id' in kwargs.keys():
            val = kwargs['category_id']
            where += 'c.id = '
        elif 'category_slug' in kwargs.keys():
            val = kwargs['category_slug']
            where += 'c.slug = '
        else:
            return None
        where += '%s'
        return {'statement': where, 'param': val}

    def basic_category_sql(self):
        '''
        basic_category_sql creates the sql code to retrieve multiple groups associated with a given
        category.  It will also return associated paragraphs and their related records

        :return: sql with the necessary elements and without where statements
        :rtype: str
        '''
        beg_sql = self.get_category_select()
        sql_tables = self.get_category_tables()
        return beg_sql + sql_tables

    def get_category_select(self):
        '''
        get_select builds the select for the given sql type (depends on how paragraphs are used)
        Sql type is set based key word args

        :param sql_type: Select part of query will be different based on value.
        :type sql_type: str
        :return: select part of the sql query
        :rtype: str
        '''
        sql = sql_sub.BEGIN_SELECT
        sql += ', ' + sql_sub.SELECT_CATEGORY + ', ' + sql_sub.SELECT_GROUP
        sql += ', ' + sql_sub.SELECT_PARAGRAPHS + ', ' + sql_sub.SELECT_REFERENCES + ' '
        return sql

    def get_category_tables(self):
        '''
        get_tables builds the tables and joins for the categories

         :return: Partial query
        :rtype: str
        '''
        sql = sql_sub.FROM_CATEGORY_JOIN_GROUP_AND_PARA
        sql += sql_sub.JOIN_REFERENCES_TO_PARA
        return sql

    def loop_through_queryset(self, query_set):
        '''
        loop_through_queryset to format data in the way needed by ParagraphsForDisplay

        :param query_set: All the paragraphs that were retrieved in queryset form
        :type query_set: django.db.models.query.RawQuerySet instance
        '''
        for row in query_set:
            if not self.category:
                self.first_row_assignments(row)
            self.process_group(row)
            self.append_unique_reference(row)
            self.append_unique_paragraph(row)

    def process_group(self, row):
        '''
        In process_group we ensure everything is set up properly, unless the group has already been
        processed

        How things work in general:
        Each category page is designed for the specific category.  We display paragraphs for a given
        group, but the paragraphs are ordered within the group and displayed by rules for the page.
        For now the only category that has different display rules are flashcards.

        If this is the first time for the given group, the following occurs:
        1. Add to list to ensure groups do not get processed more than once
        2. Adds a group dictionary to output['groups']
           a. Group data
           b. list to append the paragraphs in order (sorted in the query)
           c. list to append any link text, since references are associated with groups in display
           paragraph, but that the page associates with the group
        3. Add list to make sure that references are displayed only once for given group
        4. Add list to make sure that paragraphs are displayed only once for given group
        '''
        if row.group_id not in self.group_ids:
            self.group_ids.append(row.group_id)
            self.groups.append({'group': self.group_dictionary(row), 'paragraphs': [], 'link_text': []})
            self.group_id_to_link_text_list[row.group_id] = []
            self.group_id_to_para_ids[row.group_id] = []

    def first_row_assignments(self, row):
        '''
        first_row_assignments makes up for the fact that querysets are not normalized by
        ensuring that data we expect to be in every row is only processed in the first
        row

        :param row: All the data needed for a given paragraph, plus some repeated data
        :type row: queryset row
        '''
        self.ordered = True
        self.category = {
            'title': row.category_title,
            'id': row.category_id,
            'category_type': row.category_type,
        }

    def append_unique_reference(self, row):
        '''
        append_unique_reference ensures that even if a reference is in multiple rows, and even if it is
        it used in multiple paragraphs, it will be displayed once and only once for this group

        :param row: queryset row, not normalized!
        :type row: one row of django.db.models.query.RawQuerySet
        '''
        if row.reference_id is None:
            return
        if row.reference_id not in self.ref_ids:
            self.references.append({'link_text': row.link_text, 'url': row.url})
        if row.link_text not in self.group_id_to_link_text_list[row.group_id]:
            self.group_id_to_link_text_list[row.group_id].append(row.link_text)
            self.groups[-1]['link_text'].append(row.link_text)

    def append_unique_paragraph(self, row):
        '''
        append_unique_paragraph ensures that even if a paragraph is in multiple rows, and even if it is
        it used in multiple groups, it will be displayed once and only once for this group

        :param row: queryset row, not normalized!
        :type row: one row of django.db.models.query.RawQuerySet
        '''

        if row.paragraph_id not in self.group_id_to_para_ids[row.group_id]:
            self.group_id_to_para_ids[row.group_id].append(row.paragraph_id)
            self.groups[-1]['paragraphs'].append(self.paragraph_dictionary(row))

    def group_dictionary(self, row):
        '''
        group_dictionary is one formatted paragraph to be added to a paragraph list.  This
        dict must be in format expected by ParagraphsForDisplay

        :param row: queryset row
        :type row: one row of django.db.models.query.RawQuerySet
        :return: dictionary for one paragraph formatted in a way that works for ParagraphsForDisplay
        :rtype: dict

        [extended_summary]

        :param row: queryset row
        :type row: one row of django.db.models.query.RawQuerySet
        :return: Group db record fields, plus the unique identifier for the side menu and div id
        :rtype: [type]
        '''
        return {
            'id': row.group_id,
            'group_identifier': row.group_short_name,
            'title': row.group_title,
            'slug': row.group_slug,
            'note': row.group_note,
            'category_id': row.category_id,
        }

    def output_data(self):
        '''
        output_data is different for categories because there are many groups and one category
        The references are associated with the group, in the display
        The groups are ordered and should not be displayed individually

        :return: dictionary used to display groups and paragraphs associated with a given category
        :rtype: dict
        '''
        return {'category': self.category,
                'groups': self.groups,
                'references': self.references, }
