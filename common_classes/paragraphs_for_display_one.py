''' This class outputs a dictionary in a format used to display paragraphs.  It can be used
    for any page that either has only one group or that does not display by group.'''
from common_classes.para_display_retriever_db import ParaDisplayRetrieverDb
from common_classes.paragraphs_for_display import ParagraphsForDisplay
import constants.file_paths as file_paths


class ParagraphsForDisplayOne(ParagraphsForDisplay):
    '''
    ParagraphsForDisplayOne is used to display one pargraph record on a page and also to make
    asynchronous calls for modal popups

    The input_data is a dictionary that is formatted by a paragraph retriever object.
    Still using the para_display_retriever_db to get the data, but the output is different

    :param object: is formatted by a paragraph retriever object
    :type object: dictionary
    '''

    def retrieve_paragraphs(self, **kwargs):
        '''
        retrieve_paragraphs brings in the data necessary for the basic display paragraphs

        :return: dictionary needed to display basic paragraphs
        :rtype: dict
        '''
        self.is_modal = True if kwargs['is_modal'] else False
        retriever = ParaDisplayRetrieverDb()
        self.input_data = retriever.data_retrieval(kwargs)
        return self.format_single_para_display()

    def format_single_para_display(self):
        '''
        format_data_for_display Once we know what class to use for retrieving the input data
        this is the main driver for the formatting process

        :return: dictionary to be added to the context & used in the paragraph display template
        :rtype: dict
        '''
        self.create_links_from_references()
        self.assign_paragraphs()
        return self.output_single_para_display()

    def assign_paragraphs(self):
        '''
        assign_paragraphs - steps to create paragraph list:

        * unlike when there is a list of paragraphs, no need to sort
        1. append the paragraph values needed with the keys that are expected
        2. add the reference links that are associated with the given paragraph
        '''
        self.paragraphs = self.paragraphs_links_and_images(self.input_data['paragraphs'])
        self.add_ref_links_to_paragraphs()

    def output_single_para_display(self):
        '''
        output_for_display creates the **kwargs for the display paragraph template

        :return: final dict transformed in the study view to use in display paragraph template
        :rtype: dict
        '''
        if len(self.paragraphs) < 1:
            return ParagraphsForDisplayOne.error_output('Data not loaded for para')

        if len(self.paragraphs[0]['subtitle']) > 0:
            orig_subtitle = self.paragraphs[0]['subtitle']
        else:
            orig_subtitle = self.paragraphs[0]['short_title']
        self.paragraphs[0]['subtitle'] = orig_subtitle[:1].upper() + orig_subtitle[1:]
        if not self.is_modal:
            return self.output_page_display()
        image_url = self.create_image_url(self.paragraphs[0]['image_path'])
        if image_url:
            self.paragraphs[0]['image_path'] = self.create_image_url(self.paragraphs[0]["image_path"])
        return self.paragraphs[0]

    def create_image_url(self, image_path):
        ''' use image_path (from db) and cloudfront url to create hrefs for images '''
        if not image_path:
            return None
        return f'{file_paths.S3_CLOUDFRONT}{image_path}'

    def output_page_display(self):
        '''
        output_page_display moves the subtitle and subtitle notes to the title and title note field
        since there is no group data and we want to use the same template

        :return: paragraph that will work in the single para page view
        :rtype: dict
        '''
        single_para_for_page = {}
        single_para_for_page['title'] = self.paragraphs[0]['subtitle']
        single_para_for_page['title_note'] = self.paragraphs[0]['subtitle_note']
        self.paragraphs[0]['subtitle'] = ''
        self.paragraphs[0]['subtitle_note'] = ''
        single_para_for_page['paragraphs'] = self.paragraphs
        return single_para_for_page

    @staticmethod
    def error_output(message):
        '''
        error_output will display as a popup just like a paragraph

        :param message: will be displayed as the subtitle
        :type message: str
        :return: para format, but with message of what happened
        :rtype: dict
        '''
        return {
            'subtitle': message,
            'subtitle_note': '',
            'text': '<p>Either error or simply that something planned is not implemented yet.</p>',
            'references': 'N/A'}
