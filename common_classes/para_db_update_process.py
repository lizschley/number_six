''' This is Step Three of the database update process.  Step 1 retrieves & Step 2 edits the data '''
# pylint: pylint: disable=unused-import

import sys
import helpers.no_import_common_class.utilities as utils

from common_classes.para_db_methods import ParaDbMethods
from projects.models.paragraphs import (Category, Group,  # noqa: F401
                                        GroupParagraph, Paragraph,
                                        ParagraphReference, Reference)


class ParaDbUpdateProcess(ParaDbMethods):
    '''
        ParaDbUpdateProcess updates (or if production or run_as_prod, creates) data based on
        self.input_data
    '''

    def __init__(self, input_data, updating):
        '''
        __init__ Assign the framework needed to ...
        '''
        super(ParaDbUpdateProcess, self).__init__(updating)
        self.input_data = input_data

    def process_input_data_update_db(self):
        print(f'self.input_data=={self.input_data}')
        print(f'self.updating=={self.updating}')
        if self.input_data['run_as_prod']:
            self.prepare_run_as_prod()
        self.update_paragraph_records()
        self.add_associations()
        self.delete_associations()

    def prepare_run_as_prod(self):
        pass

    def update_paragraph_records(self):
        self.create_or_update_categories()
        self.create_or_update_references()
        self.create_or_update_paragraphs()
        self.create_or_update_groups()
        self.create_or_update_paragraph_reference()
        self.create_or_update_group_paragraph()

    def add_associations(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'add_associations'):
            return

    def delete_associations(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'delete_associations'):
            return

    def create_or_update_categories(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'categories'):
            return

    def create_or_update_references(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'references'):
            return

    def create_or_update_paragraphs(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'paragraphs'):
            return
        for para in self.input_data['file_data']['paragraphs']:
            find_dict = {'guid': para['guid']}
            new_para = self.find_and_update_record(Paragraph, find_dict, para)
            
            if utils.key_in_dictionary(new_para, 'error'):
                sys.exit(new_para['error'])
            print(f'aragraph updated: {new_para}')

    def create_or_update_groups(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'groups'):
            return

    def create_or_update_paragraph_reference(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'paragraph_reference'):
            return

    def create_or_update_group_paragraph(self):
        if utils.key_not_in_dictionary(self.input_data['file_data'], 'group_paragraph'):
            return
        for group_para in self.input_data['file_data']['group_paragraph']:
            find_dict = {'id': group_para['id']}
            new_gp = self.find_and_update_record(GroupParagraph, find_dict, group_para)
            if utils.key_in_dictionary(new_gp, 'error'):
                sys.exit(new_gp['error'])
            print(f'GroupParagraph updated: {new_gp}')
