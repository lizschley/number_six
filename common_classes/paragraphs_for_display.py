''' This class outputs a dictionary in a format used to display paragraphs.  It can be used
    for any page that either has only one group or that does not display by group.'''
import sys
import constants.common as constants
import helpers.no_import_common_class.paragraph_helpers as para_helpers
import utilities.random_methods as utils
from common_classes.para_display_retriever_cat import ParaDisplayRetrieverCat
from common_classes.para_display_retriever_db import ParaDisplayRetrieverDb
from common_classes.para_display_retriever_json import ParaDisplayRetrieverJson
from common_classes.para_display_retriever_search import ParaDisplayRetrieverSearch
from common_classes.para_link_helper import ParaLinkHelper


class ParagraphsForDisplay:
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
        self.is_modal = False
        self.group_title = ''
        self.group_note = ''
        self.group_type = ''
        self.reference_links = {}
        self.para_link_lookup = {'ref': {}, 'para': {}, 'group': {}}
        self.paragraphs = []
        self.input_data = {}

    def retrieve_paragraphs(self, **kwargs):
        '''
        retrieve_paragraphs brings in the data necessary for the displaying paragraphs

        :return: dictionary needed to display basic paragraphs
        :rtype: dict
        '''
        self.input_data = self.retrieve_input_data(kwargs)
        # import pprint
        # print('-----------------Input Data-------------------------------')
        # printer = pprint.PrettyPrinter(indent=1, width=120)
        # printer.pprint(self.input_data)
        if self.input_data is None:
            sys.exit(f'did not retrieve data with these args: {kwargs}')
        return self.format_data_for_display()

    def retrieve_input_data(self, kwargs):
        '''

        retrieve_input_data decides what class is needed to retrieve the data before formatting it
        in the way needed for the input to the paragraph display

        :param kwargs: Depending on the args the application knows what class to use for formatting
        :type kwargs: dict
        :return: the input data the this class uses for the display paragraph context
        :rtype: dict
        '''
        retriever = None
        for key in constants.VALID_DATA_RETRIEVAL_ARGS:
            if key in kwargs.keys():
                retriever = self.instantiate_class(key)
        if retriever is not None:
            return retriever.data_retrieval(kwargs)
        return None

    # Note: this will need to change once I have search and tags combined with group
    def instantiate_class(self, key):
        '''
        instantiate_class based on the key sent in, instantiates the correct paragraph retriever

        :param key: string object that represents the key of the arguments
        :type key: str
        :return: returns the object instantiated by the BaseParagraphRetriever class
        :rtype: object of type BaseParagraphRetriver
        '''
        if key == 'path_to_json':
            return ParaDisplayRetrieverJson()
        if key in constants.VALID_DB_RETRIEVER_KW_ARGS:
            return ParaDisplayRetrieverDb()
        if key in constants.VALID_CAT_RETRIEVER_ARGS:
            return ParaDisplayRetrieverCat()
        if key in constants.VALID_SEARCH_RETRIEVER_ARGS:
            return ParaDisplayRetrieverSearch()
        return None

    # Todo: make sure this is already tested.  I think it is, through an integration test
    def format_data_for_display(self):
        '''
        format_data_for_display Once we know what class to use for retrieving the input data
        this is the main driver for the formatting process

        :return: dictionary to be added to the context & used in the paragraph display template
        :rtype: dict
        '''
        message = self.check_for_errors()
        if len(message) > 3:
            return self.output_error(message)
        self.assign_group_data()
        self.create_links_from_references()
        self.assign_paragraphs()
        return self.output_for_display()

    def assign_group_data(self):
        '''
        assign_group_data, for example title; paragraph displayer has no concept of group
        '''
        group = self.input_data['group']
        self.group_title = group['group_title'].strip()
        self.group_note = group['group_note'].strip()
        self.group_type = group['group_type'].strip()

    def create_links_from_references(self):
        '''
        create_links_from_references user the link text and url to create html links
        '''
        references = self.input_data['references']
        for ref in references:
            link_text = ref['link_text'].strip()
            link = para_helpers.create_link(ref['url'], link_text)
            self.reference_links[link_text] = link.strip()
            if utils.key_not_in_dictionary(ref, 'slug'):
                continue
            slug = ref['slug']
            self.para_link_lookup['ref'][slug] = {'link_text': ref['short_text'], 'url': ref['url']}

    def assign_paragraphs(self):
        '''
        assign_paragraphs - steps to create paragraph list:

        1. sort input_paragraph list first, since it has the order field
        2. append the paragraph values needed with the keys that are expected
        3. add the reference links that are associated with the given paragraph
        '''
        input_para_list = para_helpers.sort_paragraphs(self.input_data['paragraphs'],
                                                       constants.ORDER_FIELD_FOR_PARAS)
        self.paragraphs = self.paragraphs_links_and_images(input_para_list)
        if self.input_data['para_id_to_link_text']:
            self.add_ref_links_to_paragraphs()

    def paragraphs_links_and_images(self, in_para_list):
        ''' assign_paragraphs - append the paragraph values needed with the keys that are expected '''
        kwargs = {'para_slugs': [], 'group_slugs': [],
                  'input_key': 'para_display',
                  'create_modal_links': not self.is_modal}
        link_helper = ParaLinkHelper(**kwargs)
        out_para_list = []
        for para in in_para_list:
            data = link_helper.links_from_indicators(para['text'],
                                                     self.input_data['slug_to_lookup_link'])
            para['text'] = data['text']
            para = para_helpers.add_image_information(para)
            out_para_list.append(self.paragraph(para))
        return out_para_list

    def add_ref_links_to_paragraphs(self):
        '''
        add_ref_links_to_paragraphs adds a reference string to each paragraph
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
            'slug': para['slug'],
            'short_title': para['short_title'],
            'references': '',
        }
        return para

    def output_for_display(self):
        '''
        output_for_display creates the **kwargs for the display paragraph template

        :return: final dict transformed in the study view to use in display paragraph template
        :rtype: dict
        '''
        return {'title': self.group_title,
                'title_note': self.group_note,
                'group_type': self.group_type,
                'paragraphs': self.paragraphs}

    def check_for_errors(self):
        '''
        check_for_errors makes it so a different message is displayed based on known error possibilites
        '''
        if not self.input_data['group']:
            return ('Your selection produced no results, please select something else or try '
                    'the same selection another day.')
        if self.input_data['group']['group_type'] == 'error':
            return self.input_data['group']['group_title']
        return ''


    @staticmethod
    def output_error(message):
        ''' return error message with expected key '''
        return {'error': message}
