import helpers.classes_or_scripts.paragraph_helpers as ph
from common_classes.paragraph_retriever import ParagraphRetriever


class ParagraphsForDisplay(object):
    def __init__(self):
        self.title = ''
        self.title_note = ''
        self.reference_links = {}
        self.paragraphs = []
        self.input_data = {}

    def retrieve_paragraphs(self, path_to_json=None, group_id=None, search_str=None):
        paragraphs = ParagraphRetriever()
        self.input_data = paragraphs.retrieve_input_data(path_to_json=path_to_json,
                                                         group_id=group_id,
                                                         search_str=search_str)

        if type(self.input_data) == str:
            print(f'exiting because self.input_data is a string: {self.input_data}')
            exit(0)
        return self.format_data_for_display()

    def format_data_for_display(self):
        self.assign_group_data()
        self.create_links_from_references()
        self.assign_paragraphs()
        self.sort_paragraphs()
        return self.output_for_display()

    def sort_paragraphs(self):
        pass

    def db_to_paragraph_list(self):
        # 1. get all the data
        # 2. everything will already be associated with each other
        # 3. Assign title and title_note
        # 4. Loop through paragraphs and assign the para_data, within the outer loop, do the following:
        #### 4a. create empty array for references
        #### 4b. Loop through references and create links
        pass

    def assign_group_data(self):
        group = self.input_data['group']
        self.title = group['title']
        self.title_note = group['note']

    def create_links_from_references(self):
        references = self.input_data['references']
        for ref in references:
            link_text = ref['link_text']
            link = ph.create_link(ref['url'], link_text)
            self.reference_links[link_text] = link

    def assign_paragraphs(self):
        input_list = self.input_data['paragraphs']
        for para in input_list:
            self.paragraphs.append(self.paragraph(para))
        self.add_links_to_paragraphs()

    def add_links_to_paragraphs(self):
        for para in self.paragraphs:
            para['references'] = self.paragraph_links(self.input_data['para_id_to_link_text'][para['id']])

    def paragraph_links(self, link_text_list):
        para_links = ''
        for link_text in link_text_list:
            print(link_text)
            para_links += self.reference_links[link_text] + '<br>'
        return para_links

    @staticmethod
    def paragraph(para):
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
