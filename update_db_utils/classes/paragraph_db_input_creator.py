''' writes JSON file that can be used to update the the paragraph
    structure that can be used by the ParagraphsForDisplay class db structure

    {
        "group": {"group_title": ""},
        "references": [
            {
                "link_text": "",
                "url": "",
                "short_text": ""
            }
        ],
        "paragraphs": [
            {
                "id": "",
                "subtitle": "",
                "note": "",
                "image_path": "",
                "image_info_key": "default",
                "text": "",
                "short_title": "",
                "link_text_list": []
            }
        ]
    }

    ** Important **

    Can also create the db structure directly by creating ParagraphsToDatabase and
    passing self.output directly into new_obj.dictionary_to_db(input_data)
'''
import constants.scripts as constants
from helpers.no_import_common_class.paragraph_dictionaries import ParagraphDictionaries as dictionaries
from common_classes.para_db_create_process import ParaDbCreateProcess
import utilities.json_methods as json_helper


class ParagraphDbInputCreator():
    '''
        ParagraphDbInputCreator creates JSON file of the format necessary to create
        db structure for paragraphs

        Can also create the db structure directly by creating ParagraphsToDatabase and
        passing self.output directly into new_obj.dictionary_to_db(input_data)
   '''

    def __init__(self, group_title, json_only, updating):
        '''
        __init__ creating paragraphs and possibly references from screen scraping.  Currently assuming
        that the group exists, but there is no reason a group couldn't be added.  This will be using
        the ParaDbCreateProcess class eventually, though the first step is simply to create the JSON.

        :param group_title: Group unique key, assuming that the group already exists.

        :type group_title: str
        '''

        self.output_to_json = self.base_dictionary()
        self.output_to_json['group'] = {'group_title': group_title}
        self.path_to_json = constants.INPUT_CREATE_JSON
        self.json_only = json_only
        self.updating = updating
        self.process_data = {}
        self.process_data['fake_id'] = 963963962

    def create_content(self, references, paragraphs):
        '''
        create_content creates references and paragraphs.  To associate them, it is necessary to append
        the given reference link_text with the paragraph-to-associate's link_text_list field

        :param references: references to be loaded to db
        :type references:  list
        :param paragraphs: paragraphs to be loaded to db
        :type paragraphs: list
        '''
        self.assign_references(references)
        print(f'size of input paragraphs = {len(paragraphs)}')
        print('first 30 for input')
        self.first_80(paragraphs)
        self.assign_paragraphs(paragraphs)
        print(f'size of output paragraphs = {len(self.output_to_json["paragraphs"])}')
        print('first 30 for output')
        self.first_80(self.output_to_json["paragraphs"])
        if self.json_only:
            self.write_json_file()
        else:
            self.create_records()

    def first_80(self, para_list):
        num = 0
        for para in para_list:
            num += 1
            line = para['text']
            print(f'#{num}. {line[0:80]}')


    @staticmethod
    def base_dictionary():
        ''' data structure needed for paragraph create '''
        return {
            'group': {},
            'references': [],
            'paragraphs': [],
        }

    def assign_references(self, references):
        '''
        assign_references assign references

        to assign the reference to a paragraph, need to have already appended the link_text to
        the given paragraph record array

        :param references: list of references
        :type references: list
        '''
        new_ref = dictionaries.reference_dictionary()
        for ref in references:
            self.process_data['fake_id'] += 1
            new_ref['id'] = self.process_data['fake_id']
            new_ref['link_text'] = ref['link_text']
            new_ref['url'] = ref['url']
            new_ref['short_text'] = ref['short_text']
            self.output_to_json['references'].append(ref)

    def assign_paragraphs(self, paragraphs):
        '''
        assign_paragraphs loops through list of paragraphs and makes assignments

        - gets the standalone from the group
        - no images through this process

        :param paragraphs: list of paragraphs as seen below
        :type paragraphs: list
        '''
        for para in paragraphs:
            new_para = {}
            self.process_data['fake_id'] += 1
            new_para['id'] = self.process_data['fake_id']
            new_para['subtitle'] = para['subtitle']
            new_para['note'] = para['note']
            new_para['text'] = para['text']
            new_para['short_title'] = para['short_title']
            new_para['image_path'] = para.get('image_path', '')
            new_para['image_info_key'] = para.get('image_info_key', 'default')
            new_para['link_text_list'] = para.get('link_text_list', [])
            self.output_to_json['paragraphs'].append(new_para)

    def write_json_file(self):
        ''' write_json_file writes a dictionary to the specified path '''
        json_helper.write_json_file(self.path_to_json, self.output_to_json)

    def create_records(self):
        '''
            create_records takes the screen scraped data and updates the db directly
            without running the json file using the create_paragraphs script
        '''
        paragraphs = ParaDbCreateProcess(self.updating)
        paragraphs.dictionary_to_db(self.output_to_json)
