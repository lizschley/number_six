''' writes JSON file that can be used to update the the paragraph
    structure that can be used by the ParagraphsForDisplay class db structure
    ** Important **
    Can also create the db structure directly by creating ParagraphsToDatabase and
    passing self.output directly into new_obj.dictionary_to_db(input_data)
'''
from datetime import datetime
import json
import os
import constants.scripts as constants
from portfolio.settings import BASE_DIR


OUT_JSON_PATH = os.path.join(BASE_DIR, 'data/data_for_creates')


class ParagraphDbInputCreator():
    '''
    ParagraphDbInputCreator creates JSON file of the format necessary to create
    db structure for paragraphs
    Can also create the db structure directly by creating ParagraphsToDatabase and
    passing self.output directly into new_obj.dictionary_to_db(input_data)
   '''

    def __init__(self, **kwargs):
        '''
        __init__ Assign the framework needed to easily build the dictionary used
        as input to create the paragraph structure in the db
        only title is required
        '''
        title = kwargs.get('title')
        note = kwargs.get('note', '')
        ordered = kwargs.get('ordered', 'no')
        standalone = kwargs.get('standalone', 'yes')
        self.output = self.starting_dictionary(title, note, ordered, standalone)
        self.path_to_json = ParagraphDbInputCreator.create_json_file_path()

    @staticmethod
    def reference_dictionary(link_text, url):
        '''
        reference_dictionary - helper method to create format for reference
        input to create ParagraphToDb input data
        :param link_text: text that will be link text in the reference
        :type link_text: string
        :param url: text that will be the url that is linked in the reference
        :type url: str
        :return: dictionary that is used to describe an individual reference
        :rtype: dictionary
        '''
        return {
            'link_text': link_text,
            'url': url
        }

    @staticmethod
    def paragraph_dictionary(para_id, text, subtitle='', note='', standalone=None):
        '''
        paragraph_dictionary - helper method to create format for paragraph
        input to create ParagraphToDb input data
        :param para_id: defaults to ''
        :type para_id: str
        :param subtitle: optional unless paragraph is stand-alone, defaults to ''
        :type subtitle: str
        :param text: text is input as a list of strings
        :type text: list
        :param note: always optional, defaults to ''
        :type note: str
        :return: dictionary that is a subset of ParagraphToDb input data
        :rtype: dictionary
        '''
        para = {
            'id': para_id,
            'subtitle': subtitle,
            'note': note,
            'text': text
        }
        if standalone is not None:
            para['standalone'] = standalone
        return para

    @staticmethod
    def ref_link_para_dictionary(para_id='', link_text=''):
        '''
        ref_link_para_dictionary - helper method to create format for para to reference association
        input to create ParagraphToDb input data
        :param para_id: temp_id to associate to reference, defaults to ''
        :type para_id: str
        :param link_text: [description], defaults to ''
        :type link_text: str
        :return: dictionary that is a subset of ParagraphToDb input data
        :rtype: dictionary
        '''
        return {
            'link_text': link_text,
            'paragraph_id': para_id
        }

    @staticmethod
    def starting_dictionary(title='', note='', ordered='no', standalone='yes'):
        '''
        starting_dictionary used as a helper method in creating format for input data for
        ParagraphToDb
        :param title: used for searches & for paragraph display, defaults to '' as convenience
        :type title: str, required in reality
        :param note: used for display, defaults to ''
        :type note: str, optional
        :param ordered: used to make , defaults to 'no'
        :type ordered: str, optional
        :param standalone: can be , defaults to 'yes'
        :type standalone: str, optional
        :return: [description]
        :rtype: [type]
        '''
        return {
            'group': {
                'title': title,
                'note': note,
                'ordered': ordered,
                'standalone': standalone
            },
            'references': [],
            'paragraphs': [],
            'ref_link_paragraph': []
        }

    @staticmethod
    def create_json_file_path(**kwargs):
        '''
        create_json_file_name_with_path creates json output file

        :param directory_path: directory to write to.  defaults to OUT_JSON_PATH, which is always wrong
        :type directory_path: str, optional
        :param filename: if filename is None will create filename with datetime stamp, defaults to None
        :type filename: str, optional
        :return: file_path
        :rtype: str
        '''
        prefix = kwargs.get('prefix', constants.DEFAULT_PREFIX)
        filename = kwargs.get('filename',
                              prefix + datetime.now().isoformat(timespec='seconds') + '.json')
        directory_path = kwargs.get('directory_path', OUT_JSON_PATH)

        if filename is None:
            filename = prefix + datetime.now().isoformat(timespec='seconds') + '.json'

        return directory_path + '/' + filename

    def assign_output(self, ref, para, ref_link_para):
        '''
        assign_output assigns the ref, para and ref_link_para to the outpu
        This is designed to be flexible and work with batch program.  We may have references,
        but maybe not if it is a blog or a resume
        :param ref: reference dictionary (method in this class)
        :type ref: dictionary
        :param para: paragraph dictionary (method in this class)
        :type para: [type]
        :param ref_link_para: ref_link_para dictionary (method in this class)
        :type ref_link_para: dictionary
        '''
        if ref is not None:
            self.output['references'].append(ref)
        if para is not None:
            self.output['paragraphs'].append(para)
        if ref_link_para is not None:
            self.output['ref_link_paragraph'].append(ref_link_para)

    # Todo: call RecordDictionaryUtility.write_dictionary_to_file(self.output_data, **params)
    # Todo: Combine with above (see init() - ParagraphDbInputCreator.create_json_file_path())
    def write_json_file(self):
        '''
        write_json_file writes the formatted file necessary to update the paragraph
        structure in the db
        This test mainly for testing
        '''
        with open(self.path_to_json, 'w') as file_path:
            json.dump(self.output, file_path)
