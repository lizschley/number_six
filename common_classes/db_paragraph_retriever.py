''' Derived from an abstract class containing common functionality for basic paragraph display '''
from common_classes.base_paragraph_retriever import BaseParagraphRetriever
from projects.models.paragraphs import Group

VALID_KW_ARGS = ['group_id', 'search_str', 'path_to_json']


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
        if 'group_id' not in kwargs.keys():
            return None
        query = self.write_sql()
        return self.db_output_to_display_input(Group.objects.raw(query, [kwargs['group_id']]))

    def write_sql(self):
        '''
        write_sql generates the SQL used to retrieve data

        :return: the query to be used, minus the actual group_id
        :rtype: str
        '''
        query = self.basic_sql()
        query += 'where g.id = %s'
        return query

    def basic_sql(self):
        return ('select 1 as id, g.id as group_id, title as title, g.note as title_note, '
                'gp.order, p.id as paragraph_id, subtitle, p.note as subtitle_note, text, '
                'r.id as reference_id, link_text, url '
                'from projects_group g '
                'join projects_groupparagraph gp on g.id = gp.group_id '
                'join projects_paragraph p on p.id = gp.paragraph_id '
                'join projects_paragraphreference pr on p.id = pr.paragraph_id '
                'join projects_reference r on r.id = pr.reference_id ')

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
