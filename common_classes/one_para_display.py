''' This class outputs a dictionary in a format used to display paragraphs.  It can be used
    for any page that either has only one group or that does not display by group.'''
from common_classes.db_paragraph_retriever import DbParagraphRetriever
from common_classes.paragraphs_for_display import ParagraphsForDisplay
import helpers.no_import_common_class.paragraph_helpers as para_helpers


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
            message = f'OneParaDisplay only works with subtitle as key word arg, kwargs=={kwargs}'
            return OneParaDisplay.error_output(message)

        retriever = DbParagraphRetriever()
        self.input_data = retriever.data_retrieval(kwargs)
        if self.input_data is None:
            message = f'OneParaDisplay retrieved no data with this subtitile=={kwargs["subtitle"]}'
            return OneParaDisplay.error_output(message)
        return self.format_single_para_display(kwargs['subtitle'])

    def format_single_para_display(self, subtitle):
        '''
        format_data_for_display Once we know what class to use for retrieving the input data
        this is the main driver for the formatting process

        :return: dictionary to be added to the context & used in the paragraph display template
        :rtype: dict
        '''
        self.create_links_from_references()
        self.assign_paragraphs()
        return self.output_single_para_display(subtitle)

    def assign_paragraphs(self, from_ajax=True):
        '''
        assign_paragraphs - steps to create paragraph list:

        * unlike when there is a list of paragraphs, no need to sort
        1. append the paragraph values needed with the keys that are expected
        2. add the reference links that are associated with the given paragraph
        '''

        for para in self.input_data['paragraphs']:
            para['text'] = para_helpers.replace_ajax_link_indicators(para['text'], from_ajax)
            para = para_helpers.add_image_information(para)
            self.paragraphs.append(self.paragraph(para))
        self.add_links_to_paragraphs()


    def output_single_para_display(self, subtitle):
        '''
        output_for_display creates the **kwargs for the display paragraph template

        :return: final dict transformed in the study view to use in display paragraph template
        :rtype: dict
        '''
        if len(self.paragraphs) < 1:
            return OneParaDisplay.error_output(f'Data not yet loaded for subtitle=={subtitle}')
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
            'text': '<p>Either error or simply that something planned is not implemented yet.</p>',
            'references': 'N/A'}
