'''Abstract class used in formatting correct data for the basic paragraph display'''
from abc import ABC, abstractmethod


class ParaDisplayRetrieverBase(ABC):
    '''
    ParaDisplayRetrieverBase is an abstract class used to create input data for ParagraphsForDisplay
    This ensures that even if the datasource varies, the paragraphs will still display correctly.

    :param ABC: Pythons Abstract Base Class
    :type ABC: Class of type ABC
    '''
    def __init__(self):
        # for processing db retrieval, not needed for demo (JSON to display)
        self.ordered = False
        # for output
        self.group = {}
        self.references = []
        self.paragraphs = []
        self.para_id_to_link_text = {}
        self.slug_to_lookup_link = {'para_slug_to_short_title': {},
                                    'ref_slug_to_reference': {},
                                    'group_slug_to_short_name': {}, }

    @abstractmethod
    def data_retrieval(self, kwargs):
        '''
        data_retrieval can not be implemented, because we do not know how to import the data

        :param kwargs: [description]
        :type kwargs: [type]
        '''

    def get_paragraph_order(self, subtitle, order):
        '''
        get_paragraph_order will use standard process to define the paragraph order

        :param subtitle: default order
        :type subtitle: str
        :param order: can be used for paragraphs that need to be ordered within a group
        :type order: str
        :return: will return a field that can be used for sorting paragraphs
        :rtype: str
        '''
        return order if self.ordered else subtitle.lower()

    def process_ref_link_paragraph(self, ref_link_para):
        '''
        process_ref_link_paragraph loops through paragraph to reference association data to
        create a dictionary that uses the paragraph id (primary key from db retrieval or any unique
        string when using a dictionary from a JSON file) to associate a paragraph with zero-to-many
        reference.  References are represented by the reference link_text, unique for references.

        :param ref_link_para: paragraph to references association input
        :type ref_link_para: dict
        '''
        for rlp in ref_link_para:
            self.add_ref_to_paragraph_link_txt_dictionary(rlp['paragraph_id'], rlp['link_text'])

    def add_ref_to_paragraph_link_txt_dictionary(self, para_id, link_text):
        '''
        add_ref_to_paragraph_link_txt_dictionary creates a new para_id to link_text
        association.  If the para_id key does not exist, it needs to add the key as well.
        Have to be careful not to replace the existing relationship.

        :param para_id: paragraph record primary key to str or made up str if displaying from JSON
        :type para_id: str
        :param link_text: unique identifier for reference
        :type link_text: str
        '''
        if para_id in self.para_id_to_link_text.keys():
            self.para_id_to_link_text[para_id].append(link_text)
        else:
            self.para_id_to_link_text[para_id] = [link_text]

    def output_data(self):
        '''
        output_data is the data used to display paragraphs however the paragraphs
        are derived

        :return: dictionary used to display paragraphs
        :rtype: dict
        '''
        return {'group': self.group,
                'references': self.references,
                'paragraphs': self.paragraphs,
                'para_id_to_link_text': self.para_id_to_link_text,
                'slug_to_lookup_link': self.slug_to_lookup_link,
                }
