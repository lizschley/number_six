from projects.models.paragraphs import Group
import helpers.classes_or_scripts.paragraph_helpers as ph

VALID_KW_ARGS = ['group_id', 'search_str', 'path_to_json']


class ParagraphRetriever(object):
    def __init__(self):
        # for input
        self.group_id = None
        self.search_str = None
        self.path_to_json = None
        # for processing db retrieval, not needed for demo (JSON to display)
        self.ordered = False
        # for output
        self.group = {}
        self.para_id_to_link_text = {}
        self.paragraphs = []
        self.references = []

    def retrieve_input_data(self, path_to_json=None, group_id=None, search_str=None):
        self.group_id = group_id
        self.path_to_json = path_to_json
        self.search_str = search_str
        if self.group_id is not None and self.search_str is None:
            return self.group_id_only()
        elif self.group_id is not None and self.search_str is not None:
            return 'not implemented'
        elif self.search_str is not None:
            return 'not implemented'
        elif self.path_to_json is not None:
            return self.json_path_to_display_input()
        else:
            return 'All standalone is not yet implemented'

    def group_id_only(self):
        query = self.basic_sql()
        query += ' where g.id = %s'
        query += ' order by gp.order, p.subtitle'
        return self.db_output_to_display_input(Group.objects.raw(query, [self.group_id]))

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

    def db_output_to_display_input(self, raw_queryset):
        return 'not implemented'

    def json_path_to_display_input(self):
        input_data = ph.json_to_dict(self.path_to_json)
        self.group = input_data['group']
        self.process_json_paragraphs(input_data['paragraphs'])
        self.references = input_data['references']
        self.process_ref_link_paragraph(input_data['ref_link_paragraph'])
        return self.output_data()

    def process_json_paragraphs(self, orig_paragraphs):
        for orig_para in orig_paragraphs:
            para = self.format_paragraph(orig_para)
            self.paragraphs.append(para)

    def format_paragraph(self, orig_para):
        para = orig_para
        para['text'] = ph.format_json_text(orig_para['text'])
        para['order'] = self.get_paragraph_order(orig_para)
        return para

    def get_paragraph_order(self, para):
        return para['order'] if self.ordered else para['subtitle'].lower()

    def process_ref_link_paragraph(self, ref_link_para):
        for rlp in ref_link_para:
            if rlp['paragraph_id'] in self.para_id_to_link_text.keys():
                self.para_id_to_link_text[rlp['paragraph_id']].append(rlp['link_text'])
            else:
                self.para_id_to_link_text[rlp['paragraph_id']] = [rlp['link_text']]
        print(f'para_id_to_link_text == {self.para_id_to_link_text}')

    def output_data(self):
        return {'group': self.group,
                'references': self.references,
                'paragraphs': self.paragraphs,
                'para_id_to_link_text': self.para_id_to_link_text,}

