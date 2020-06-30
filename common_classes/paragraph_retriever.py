from projects.models.paragraphs import Group
import helpers.no_import_common_class.paragraph_helpers as ph

VALID_KW_ARGS = ['group_id', 'search_str', 'path_to_json']


class ParagraphRetriever():
    ''' The ParagraphRetriever class retrieves the information to use to output paragraphs.'''

    def __init__(self):
        # for processing db retrieval, not needed for demo (JSON to display)
        self.ordered = False
        self.para_ids = []
        self.ref_ids = []
        # for output
        self.group = {}
        self.para_id_to_link_text = {}
        self.paragraphs = []
        self.references = []

    def retrieve_input_data(self, **kwargs):
        ''' this is a generic function that allows kwargs to be automatically assigned '''
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

        # print(f'self.__dict__ == {self.__dict__}')
        return self.data_retrieval()

    def data_retrieval(self):
        ''' This will probably go away after refactoring '''
        if hasattr(self, 'group_id') and not hasattr(self, 'search_str'):
            return self.group_id_only()
        elif hasattr(self, 'group_id') and hasattr(self, 'search_str'):
            return 'not implemented'
        elif hasattr(self, 'search_str'):
            return 'not implemented'
        elif hasattr(self, 'path_to_json'):
            return self.json_path_to_display_input()
        else:
            return 'All standalone is not yet implemented'

    def group_id_only(self):
        query = self.basic_sql()
        query += ' where g.id = %s'
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
        # for row in raw_queryset:
        #     print(f'group_id == {row.group_id}')
        #     print(f'title == {row.title}')
        #     print(f'title_note == {row.title_note}')
        #     print(f'order == {row.order}')
        #     print(f'para_id == {row.paragraph_id}')
        #     print(f'subtitle == {row.subtitle}')
        #     print(f'subtitle note == {row.subtitle_note}')
        #     print(f'ref_id == {row.reference_id}')
        #     print(f'link text == {row.link_text}')
        self.loop_through_queryset(raw_queryset)
        return self.output_data()

    def loop_through_queryset(self, query_set):
        ''' turn the queryset into a dictionary used for a paragraph display '''
        for row in query_set:
            if not self.group:
                self.first_row_assignments(row)
            self.add_ref_to_paragraph_link_txt_dictionary(row.paragraph_id, row.link_text)
            self.append_unique_reference(row)
            self.append_unique_paragraph(row)

    def first_row_assignments(self, row):
        self.ordered = False if row.order == 0 else True
        self.group = {
            'title': row.title,
            'note': row.note,
        }

    def append_unique_reference(self, row):
        if row.reference_id not in self.ref_ids:
            self.references.append({'link_text': row.link_text, 'url': row.url})
            self.ref_ids.append(row.reference_id)

    def append_unique_paragraph(self, row):
        if row.paragraph_id not in self.para_ids:
            self.paragraphs.append(self.paragraph_dictionary(row))
            self.para_ids.append(row.paragraph_id)

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
        para['order'] = self.get_paragraph_order(orig_para['subtitle'], 0)
        return para

    def paragraph_dictionary(self, row):
        return {
            'id': row.paragraph_id,
            'subtitle': row.subtitle,
            'note': row.subtitle_note,
            'text': row.text,
            'order': self.get_paragraph_order(row.subtitle, row.order),
        }

    def get_paragraph_order(self, subtitle, order):
        return order if self.ordered else subtitle.lower()

    def process_ref_link_paragraph(self, ref_link_para):
        for rlp in ref_link_para:
            self.add_ref_to_paragraph_link_txt_dictionary(rlp['paragraph_id'], rlp['link_text'])

    def add_ref_to_paragraph_link_txt_dictionary(self, para_id, link_text):
        if para_id in self.para_id_to_link_text.keys():
            self.para_id_to_link_text[para_id].append(link_text)
        else:
            self.para_id_to_link_text[para_id] = [link_text]

    def output_data(self):
        # print('in output data')
        # print(f'group is {self.group}')
        # print(f'references are {self.references}')
        # print(f'paragraphs are {self.paragraphs}')
        return {'group': self.group,
                'references': self.references,
                'paragraphs': self.paragraphs,
                'para_id_to_link_text': self.para_id_to_link_text, }
