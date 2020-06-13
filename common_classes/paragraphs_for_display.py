import helpers.paragraph_helpers as ph


class ParagraphsForDisplay(object):
    def __init__(self):
        self.title = ''
        self.title_note = ''
        self.reference_links = {}
        self.paragraphs = []

    def dictionary_to_paragraph_list(self, input_data):
        self.assign_group_data(input_data)
        self.create_links_from_references(input_data)
        self.assign_paragraphs(input_data)
        return self.output_for_display()

    def db_to_paragraph_list(self, input_data):
        # 1. get all the data
        # 2. everything will already be associated with each other
        # 3. Assign title and title_note
        # 4. Loop through paragraphs and assign the para_data, within the outer loop, do the following:
        #### 4a. create empty array for references
        #### 4b. Loop through references and create links
        pass

    def assign_group_data(self, input_data):
        group = input_data['group']
        self.title = group['title']
        self.title_note = group['note']

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
            para['text'] = ph.format_json_text(para['text'])
            self.paragraphs.append(self.paragraph(para))
        self.add_links_to_paragraphs(input_data)

    def add_links_to_paragraphs(self, input_data):
        ref_para = input_data['ref_link_paragraph']
        for para in self.paragraphs:
            associations = list(filter(lambda ref_par: para['id'] == ref_par['paragraph_id'], ref_para))
            para['references'] = self.paragraph_links_from_associations(associations)

    def paragraph_links_from_associations(self, associations):
        para_links = ''
        for assoc in associations:
            para_links += self.reference_links[assoc['link_text']] + '<br>'

        return para_links

    def paragraph(self, para):
        para = {
            'id': para['id'],
            'subtitle': para['subtitle'],
            'subtitle_note': para['note'],
            'text': para['text'],
            'references': '',
        }
        return para

    def output_for_display(self):
        out = {'title': self.title,
               'title_note': self.title_note,
               'paragraphs': self.paragraphs,
              }
        return out
