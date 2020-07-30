''' This class outputs a dictionary in a format used to display paragraphs.  It can be used
    for any page that either has only one group or that does not display by group.'''
import constants.common as constants
import helpers.no_import_common_class.paragraph_helpers as para_helpers
from common_classes.db_paragraph_retriever import DbParagraphRetriever
from common_classes.paragraphs_for_display import ParagraphsForDisplay


# Todo: extend this to make SingleParaDisplay
class OneParaDisplay(ParagraphsForDisplay):
    '''
    OneParaDisplay is used for Ajax calls to display a definition or whatever

    The input_data is a dictionary that is formatted by a paragraph retriever object.
    Still using the db_paragraph_retriever to get the data, but the output is different

    :param object: is formatted by a paragraph retriever object
    :type object: dictionary
    '''

    # def __init__(self):
    #     super().__init__()  # in Python 2 use super(D, self).__init__()

    def retrieve_paragraphs(self, **kwargs):
        '''
        retrieve_paragraphs brings in the data necessary for the basic display paragraphs

        :return: dictionary needed to display basic paragraphs
        :rtype: dict
        '''
        if not kwargs['subtitle']:
            message = f'OneParaDisplay only works with subtitle as kwargs, kwargs== {kwargs}'
            return OneParaDisplay.error_output(message)

        retriever = DbParagraphRetriever()
        self.input_data = retriever.data_retrieval(kwargs)
        if self.input_data is None:
            message = f'OneParaDisplay retrieved no data with this subtitile=={kwargs["subtitle"]}'
            return OneParaDisplay.error_output(message)
        return self.format_data_for_display(kwargs['subtitle'])

    # Todo: make sure this is already tested.  I think it is, through an integration test
    def format_data_for_display(self, subtitle):
        '''
        format_data_for_display Once we know what class to use for retrieving the input data
        this is the main driver for the formatting process

        :return: dictionary to be added to the context & used in the paragraph display template
        :rtype: dict
        '''
        self.create_links_from_references()
        self.assign_paragraphs()
        return self.output_for_display(subtitle)

    def create_links_from_references(self):
        '''
        create_links_from_references user the link text and url to create html links
        '''
        references = self.input_data['references']
        for ref in references:
            link_text = ref['link_text'].strip()
            link = para_helpers.create_link(ref['url'], link_text)
            self.reference_links[link_text] = link.strip()

    def assign_paragraphs(self):
        '''
        assign_paragraphs - steps to create paragraph list:

        1. sort input_paragraph list first, since it has the order field
        2. append the paragraph values needed with the keys that are expected
        3. add the reference links that are associated with the given paragraph
        '''
        input_para_list = para_helpers.sort_paragraphs(self.input_data['paragraphs'],
                                                       constants.ORDER_FIELD_FOR_PARAS)
        for para in input_para_list:

            self.paragraphs.append(self.paragraph(para))
        self.add_links_to_paragraphs()

    def add_links_to_paragraphs(self):
        '''
        add_links_to_paragraphs adds a reference string to each paragraph
        '''
        for para in self.paragraphs:
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
            'references': '',
        }
        return para

    def output_for_display(self, subtitle):
        '''
        output_for_display creates the **kwargs for the display paragraph template

        :return: final dict transformed in the study view to use in display paragraph template
        :rtype: dict
        '''
        if len(self.paragraphs) < 1:
            return OneParaDisplay.error_output(f'No data for for subtitle=={subtitle}')
        para = self.paragraphs[0]
        orig_subtitle = para['subtitle']
        para['subtitle'] = orig_subtitle[:1].upper() + orig_subtitle[1:]
        return para

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
            'text': '<p>Have not loaded data</p>',
            'references': 'N/A'}
