''' Derived from an abstract class containing common functionality for basic paragraph display '''
import constants.sql_substrings as sql_sub
import constants.common as constants
from common_classes.para_db_methods import ParaDbMethods
from common_classes.para_display_retriever_db import ParaDisplayRetrieverDb
import helpers.no_import_common_class.utilities as utils
from projects.models.paragraphs import (Category)


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
            self.groups = {'group_slug': {'group': {}, 'paragraphs': [], 'link_text': []}}
        '''
        super().__init__()
        # for output (also self.references, unchanged from base class)
        self.category = {}
        self.groups = {}

    def data_retrieval(self, kwargs):
        '''
        data_retrieval is to retrieve data from the database when the paragraphs associated with a group
        are displayed together based on the paragraph order.

        :param kwargs: currently just category_id
        :type kwargs: dict
        :return: a dictionary in the format that works with the standard ParagraphsForDisplayCat
        :rtype: dict
        '''
        if 'category_id' in kwargs.keys():
            query = self.write_category_sql()
            raw_queryset = ParaDbMethods.class_based_rawsql_retrieval(query, Category,
                                                                      kwargs['category_id'])
            return self.db_output_to_display_input(raw_queryset)
        return None

    # Todo: change not standalone to category null and not in EXCLUDE_FROM_STUDY_GROUPS
    def write_category_sql(self):
        '''
        write_group_standalone_para_sql generates the SQL used to retrieve data when it is retrieved
        using a group and the paragraphs are standalone

        :return: the query to be used, minus the actual group_id
        :rtype: str
        '''
        query = self.build_category_sql()
        query += 'where c.id = %s '
        query += 'order by g.id, gp.order'
        return query

    def build_category_sql(self):
        '''
        build_category_sql creates the sql code to retrieve multiple groups associated with a given
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
        sql = sql_sub.FROM_CATEGORY_JOIN_GROUP + sql_sub.JOIN_GROUP_TO_PARA
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
        return self.output_data()

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
        process_group needs to get the group identifier which is used on the display page as link_text
        If a group with the given slug has already been processed, then nothing happens.

        if this is the first time for the given group, the following occurs:
        1. Creates group dictionary that includes the group identifier, along with the db record fields
        2. Adds an empty array to append the paragraphs in order (sorted in the query)
        3. Adds an empty array to append any references, which are associated with the entire group
        '''
        if utils.key_not_in_dictionary(self.group, row.group_id):
            group_identifier = constants.EXERCISE_GROUP_IDENTIFIERS[row.group_slug]
            group_dict = self.group_dictionary(row, group_identifier)
            self.group[row.group_id] = {'group': group_dict, 'paragraphs': [], 'link_text': []}

    def add_ref_to_group_link_txt_dictionary(self, group_id, link_text):
        '''
        add_ref_to_group_link_txt_dictionary associates references to groups.  If the group_id key
        does not exist, it needs to add the key as well.
        Have to be careful not to replace the existing relationship.

        :param group_id: group record primary key to str or made up str if displaying from JSON
        :type group_id: str
        :param link_text: unique identifier for reference
        :type link_text: str
        '''
        if link_text not in self.group[group_id]['link_text']:
            self.group[group_id].append(link_text)

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
            self.group[row.group_id]['paragraphs'].append(self.paragraph_dictionary(row))
            self.para_ids.append(row.paragraph_id)

    def paragraph_dictionary(self, row):
        '''
        paragraph_dictionary is one formatted paragraph to be added to a paragraph list.  This
        dict must be in format expected by ParagraphsForDisplay

        :param row: queryset row
        :type row: one row of django.db.models.query.RawQuerySet
        :return: dictionary for one paragraph formatted in a way that works for ParagraphsForDisplay
        :rtype: dict
        '''
        order = row.order
        return {
            'id': row.paragraph_id,
            'subtitle': row.subtitle,
            'note': row.subtitle_note,
            'text': row.text,
            'image_path': row.image_path,
            'image_info_key': row.image_info_key,
            'order': self.get_paragraph_order(row.subtitle, order),
        }

    def group_dictionary(self, row, group_identifier):
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
        :param group_identifier: identifier - will be div_id and link text on a side menu on categories page
        :type group_identifier: string
        :return: Group db record fields, plus the unique identifier for the side menu and div id
        :rtype: [type]
        '''
        return {
            'id': row.group_id,
            'group_identifier': group_identifier,
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
        print('in output data')
        print(f'group is {self.group}')
        print(f'references are {self.references}')
        return {'categories': self.category,
                'group': self.group,
                'references': self.references, }


