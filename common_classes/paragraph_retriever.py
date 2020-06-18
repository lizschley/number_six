from projects.models.paragraphs import Group

VALID_KW_ARGS = ['group_id', 'category_id', 'search_str', 'tags', 'path_to_json']


class ParagraphRetriever(object):
    def __init__(self, **kwargs):
        self.group_id = kwargs['group_id']
        self.category_id = kwargs['category_id']
        self.search_str = kwargs['search_str']
        self.path_to_json = kwargs['path_to_json']

    def return_formatted_input_to_display(self):
        if self.group_id is not None and self.search_str is None:
            return self.group_id_only()
        if self.category_id is not None and self.search_str is None:
            return 'not implemented'
        if self.group_id is not None and self.search_str is not None:
            return 'not implemented'
        if self.category_id is not None and self.search_str is not None:
            return 'not implemented'
        if self.search_str is not None:
            return 'not implemented'
        if self.path_to_json is not None:
            return self.json_path()
        return 'All standalone is not yet implemented'

    def group_id_only(self):
        query = self.basic_sql()
        query += ' where g.id = %s'
        query += ' order by gp.order, p.subtitle'
        return self.db_output_to_display_input(Group.objects.raw(query, [self.group_id]))

    def db_output_to_display_input(self, raw_queryset):
        pass

    def basic_sql(self):
        query = ''' select 1 as id, g.id as group_id, title as title, g.note as title_note,  
                               gp.order, p.id as paragraph_id, subtitle, p.note as subtitle_note, text,
                               r.id as reference_id, link_text, url
                        from
                               projects_group g
                        join projects_groupparagraph gp on g.id = gp.group_id
                        join projects_paragraph p on p.id = gp.paragraph_id
                        join projects_paragraphreference pr on p.id = pr.paragraph_id
                        join projects_reference r on r.id = pr.reference_id
                    '''
        return query

    def json_path(self, path):
        pass
