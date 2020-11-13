''' This class outputs a dictionary in a format used to display paragraphs.  It can be used
    for any page that either has only one group or that does not display by group.'''
from common_classes.para_display_retriever_db import ParaDisplayRetrieverDb
from common_classes.paragraphs_for_display import ParagraphsForDisplay
import helpers.no_import_common_class.paragraph_helpers as para_helpers


class ParagraphsForDisplayOne(ParagraphsForDisplay):
    '''
    ParagraphsForDisplayOne is used for Ajax calls to display a definition or whatever

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
        if not kwargs['subtitle']:
            message = ('ParagraphsForDisplayOne only works with subtitle as key word arg, '
                       f'kwargs=={kwargs}')
            return ParagraphsForDisplayOne.error_output(message)

        retriever = ParaDisplayRetrieverDb()
        self.input_data = retriever.data_retrieval(kwargs)
        if self.input_data is None:
            message = ('ParagraphsForDisplayOne retrieved no data with this '
                       f'subtitle=={kwargs["subtitle"]}')
            return ParagraphsForDisplayOne.error_output(message)
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
        inline_args = ParagraphsForDisplay.INLINE_ARGS
        ajax_args = ParagraphsForDisplay.AJAX_ARGS
        ajax_args['from_ajax'] = from_ajax
        for para in self.input_data['paragraphs']:
            para['text'] = para_helpers.replace_link_indicators(para_helpers.inline_link,
                                                                para['text'], **inline_args)
            para['text'] = para_helpers.replace_link_indicators(para_helpers.ajax_link,
                                                                para['text'], **ajax_args)
            para = para_helpers.add_image_information(para)
            self.paragraphs.append(self.paragraph(para))
        self.add_ref_links_to_paragraphs()

    def output_single_para_display(self, subtitle):
        '''
        output_for_display creates the **kwargs for the display paragraph template

        :return: final dict transformed in the study view to use in display paragraph template
        :rtype: dict
        '''
        if len(self.paragraphs) < 1:
            return ParagraphsForDisplayOne.error_output(f'Data not yet loaded for subtitle=={subtitle}')
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
