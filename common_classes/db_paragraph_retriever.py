''' Derived from an abstract class containing common functionality for basic paragraph display '''
from common_classes.base_paragraph_retriever import BaseParagraphRetriever
from projects.models.paragraphs import Group
from projects.models.paragraphs import Paragraph
import constants.common as constants

VALID_KW_ARGS = ['group_id', 'search_str', 'para_id']


class DbParagraphRetriever(BaseParagraphRetriever):
    ''' The DbParagraphRetriever class retrieves the information to use to output paragraphs.  Later
        there may be other flavors, such as a blog or flash cards'''

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
            query = self.write_group_standalone_para_sql()
            return self.db_output_to_display_input(Group.objects.raw(query, [kwargs['group_id']]))
        if 'para_id' in kwargs.keys():
            self.group = {'title': f'para_id={str(kwargs["para_id"])}', 'note': ''}
            query = self.write_one_standalone_para_sql()
            return self.db_output_to_display_input(Paragraph.objects.raw(query, [kwargs['para_id']]))
        return None

    def write_group_standalone_para_sql(self):
        '''
        write_group_standalone_para_sql generates the SQL used to retrieve data when it is retrieved
        using a group and the paragraphs are standalone

        :return: the query to be used, minus the actual group_id
        :rtype: str
        '''
        query = self.build_basic_sql('group_id_only')
        query += 'where g.id = %s'
        query += ' and p.standalone = TRUE'
        return query

    def write_one_standalone_para_sql(self):
        '''
        write_one_standalone_para_sql generates the SQL used to retrieve data when it is retrieved
        using a paragraph_id

        :return: the query to be used, minus the actual para_id
        :rtype: str
        '''
        query = self.build_basic_sql('para_id')
        query += 'where p.id = %s'
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
        sql = constants.BEGIN_SELECT
        if sql_type == 'group_id_only':
            sql += ', ' + constants.SELECT_GROUP
        sql += ', ' + constants.SELECT_PARAGRAPHS + ', ' + constants.SELECT_REFERENCES + ' '
        return sql

    def get_tables(self, sql, sql_type):
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
        self.ordered = row.order != 0
        self.group = {
            'title': row.title,
            'note': row.note,
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

    def paragraph_dictionary(self, row):
        '''
        paragraph_dictionary is one formatted paragraph to be added to a paragraph list.  This
        dict must be in format expected by ParagraphsForDisplay

        :param row: queryset row
        :type row: one row of django.db.models.query.RawQuerySet
        :return: dictionary for one paragraph formatted in a way that works for ParagraphsForDisplay
        :rtype: dict
        '''
        return {
            'id': row.paragraph_id,
            'subtitle': row.subtitle,
            'note': row.subtitle_note,
            'text': row.text,
            'order': self.get_paragraph_order(row.subtitle, row.order),
        }
