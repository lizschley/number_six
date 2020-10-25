''' This class outputs a dictionary in a format used to display paragraphs.  It can be used
    for any page that either has only one group or that does not display by group.'''
import constants.common as constants
import helpers.no_import_common_class.paragraph_helpers as para_helpers
from common_classes.paragraphs_for_display import ParagraphsForDisplay


class ParagraphsForDisplayCat(ParagraphsForDisplay):
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
        super().__init__()
        # self.title = ''
        # self.title_note = ''
        # self.reference_links = {}
        # self.paragraphs = []
        # self.input_data = {}
        self.groups = []  # ????

    # Todo: make sure this is already tested.  I think it is, through an integration test
    def format_data_for_display(self):
        '''
        format_data_for_display Once we know what class to use for retrieving the input data
        this is the main driver for the formatting process

        :return: dictionary to be added to the context & used in the paragraph display template
        :rtype: dict
        '''
        self.assign_group_data()
        self.create_links_from_references()
        self.assign_paragraphs()
        return self.output_for_display()

    def assign_group_data(self):
        '''
        assign_group_data, for example title; paragraph displayer has no concept of group
        '''
        group = self.input_data['group']
        self.title = group['title'].strip()
        self.title_note = group['note'].strip()

    def create_links_from_references(self):
        '''
        create_links_from_references user the link text and url to create html links
        '''
        references = self.input_data['references']
        for ref in references:
            link_text = ref['link_text'].strip()
            link = para_helpers.create_link(ref['url'], link_text)
            self.reference_links[link_text] = link.strip()

    def assign_paragraphs(self, from_ajax=False):
        '''
        assign_paragraphs - steps to create paragraph list:

        1. sort input_paragraph list first, since it has the order field
        2. append the paragraph values needed with the keys that are expected
        3. add the reference links that are associated with the given paragraph
        '''
        input_para_list = para_helpers.sort_paragraphs(self.input_data['paragraphs'],
                                                       constants.ORDER_FIELD_FOR_PARAS)
        for para in input_para_list:
            para['text'] = para_helpers.replace_ajax_link_indicators(para['text'], from_ajax)
            para = para_helpers.add_image_information(para)
            self.paragraphs.append(self.paragraph(para))
        if self.input_data['para_id_to_link_text']:
            self.add_links_to_paragraphs()

    def add_links_to_paragraphs(self):
        '''
        add_links_to_paragraphs adds a reference string to each paragraph
        '''
        for para in self.paragraphs:
            if self.input_data['para_id_to_link_text'].get(para['id']) is None:
                continue
            para['references'] = self.paragraph_links(
                self.input_data['para_id_to_link_text'][para['id']])

    def paragraph_links(self, link_text_list):
        '''
        paragraph_links formats the references for a given parragraph

        :param link_text_list: takes a list of the link_text associated with the current paragraph
        :type link_text_list: list
        :return: list of the html links assoicated with the paragraph (separated with html new_line)
        :rtype: list of strings
        '''
        para_links = ''
        for link_text in link_text_list:
            para_links += self.reference_links[link_text] + '<br>'
        return para_links

    @staticmethod
    def paragraph(para):
        '''
        paragraph is the format of a given paragraph expected in the paragraph display template

        :param para: one paragraph formatted as in input data
        :type para: dict
        :return: one paragraph formatted as needed in the paragraph display template
        :rtype: dict
        '''
        para = {
            'id': para['id'],
            'subtitle': para['subtitle'],
            'subtitle_note': para['note'],
            'text': para['text'],
            'image_path': para['image_path'],
            'image_classes': para['image_classes'],
            'image_alt': para['image_alt'],
            'references': '',
        }
        return para

    def output_for_display(self):
        '''
        output_for_display creates the **kwargs for the display paragraph template

        :return: final dict transformed in the study view to use in display paragraph template
        :rtype: dict
        '''
        return {'title': self.title,
                'title_note': self.title_note,
                'paragraphs': self.paragraphs}
