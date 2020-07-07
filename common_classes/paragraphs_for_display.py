''' This class outputs a dictionary in a format used to display paragraphs.  It can be used
    for any page that either has only one group or that does not display by group.'''

import os

import helpers.no_import_common_class.paragraph_helpers as ph
from common_classes.paragraph_retriever import ParagraphRetriever


class ParagraphsForDisplay(object):
    '''
    ParagraphsForDisplay is used to create the context for the paragraph display views

    Title and title_note are added directly to the context, whereas the reference links
    are turned into html code that are are links to references that are associated
    with each paragraph.  The paragraph list will also be added directly to the context.

    The input_data is a dictionary that is formatted by a paragraph retriever object.
    The plans are for different flavors of retrievers, based on the storage format.

    :param object: is formatted by a paragraph retriever object
    :type object: dictionary
    '''
    def __init__(self):
        self.title = ''
        self.title_note = ''
        self.reference_links = {}
        self.paragraphs = []
        self.input_data = {}

    # Review: this is a great candidate for refactoring.  Based on parameters will
    # call different a flavor of paragraph retriever
    def retrieve_paragraphs(self, path_to_json=None, group_id=None, search_str=None):
        ''' this will change '''
        paragraphs = ParagraphRetriever()
        self.input_data = paragraphs.retrieve_input_data(path_to_json=path_to_json,
                                                         group_id=group_id,
                                                         search_str=search_str)
        print(f'after retrieve, input_data == {self.input_data}')

        # Todo: change this to standard error handling
        if isinstance(self.input_data, str):
            print(f'exiting because self.input_data is a string: {self.input_data}')
            os._exit(1)
        return self.format_data_for_display()

    # Todo: use mock for this unit test
    def format_data_for_display(self):
        self.assign_group_data()
        self.create_links_from_references()
        self.assign_paragraphs()
        self.sort_paragraphs()
        return self.output_for_display()

    # Todo: implement sort -> paragraphs list, sorted by the sort field(sort_num or subtitle)
    def sort_paragraphs(self):
        pass

    def assign_group_data(self):
        group = self.input_data['group']
        self.title = group['title'].strip()
        self.title_note = group['note'].strip()

    def create_links_from_references(self):
        references = self.input_data['references']
        for ref in references:
            link_text = ref['link_text'].strip()
            link = ph.create_link(ref['url'], link_text)
            self.reference_links[link_text] = link.strip()

    def assign_paragraphs(self):
        input_list = self.input_data['paragraphs']
        for para in input_list:
            self.paragraphs.append(self.paragraph(para))
        self.add_links_to_paragraphs()

    def add_links_to_paragraphs(self):
        for para in self.paragraphs:
            para['references'] = self.paragraph_links(
                self.input_data['para_id_to_link_text'][para['id']])

    def paragraph_links(self, link_text_list):
        para_links = ''
        for link_text in link_text_list:
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
