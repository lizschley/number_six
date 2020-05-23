import utilities.paragraph_helpers as ph


class ParagraphsForDisplay(object):
    def __init__(self):
        self.title = ''
        self.title_note = ''
        self.reference_links = {}
        self.paragraph_reference_links = {}
        self.paragraphs = []
        self.stand_alone = True
        self.group_id = 0

    def db_params_to_paragraph_list(self, *kwargs):
        return self.dict_to_paragraph_list(self.input_data_from_db(kwargs))

    def input_data_from_db(self, args):
        print(f'kw args == {args}')
        return {}

    def dict_to_paragraph_list(self, input_data):
        self.assign_group_data(input_data)
        self.create_links_from_references(input_data)
        self.assign_paragraphs(input_data)
        return self.output_for_display()

    def assign_group_data(self, input_data):
        group = input_data['group']
        self.title = group['title']
        self.title_note = group['note']
        self.stand_alone = True if group['stand_alone'] == 'yes' else False

    def create_links_from_references(self, input_data):
        references = input_data['references']
        for ref in references:
            link_text = ref['link_text']
            link = ph.create_link(ref['url'], link_text)
            self.reference_links[link_text] = link

    def assign_paragraphs(self, input_data):
        para_list = input_data['paragraphs']
        self.paragraphs = []
        for para in para_list:
            self.paragraphs.append(self.paragraph(para))
        self.add_links_to_paragraphs(input_data)

    def add_links_to_paragraphs(self, input_data):
        ref_para = input_data['ref_link_paragraph']
        for para in self.paragraphs:
            associations = list(filter(lambda ref_par: para['id'] == ref_par['paragraph_id'], ref_para))
            para['references'] = self.paragraph_links_from_associations(associations)

    def paragraph_links_from_associations(self, associations):
        para_links = []
        for assoc in associations:
            para_links.append(self.reference_links[assoc['link_text']])
        return para_links

    def paragraph(self, para):
        para = {
            'id': para['id'],
            'subtitle': para['subtitle'],
            'subtitle_note': para['note'],
            'text': para['text'],
            'stand_alone': self.stand_alone,
            'references': [],
        }
        return para

    def output_for_display(self):
        out = {'title': self.title,
               'title_note': self.title_note,
               'paragraphs': self.paragraphs,
              }
        return out
