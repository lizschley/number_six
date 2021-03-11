''' This is Step Three of the database update process.  Step 1 retrieves & Step 2 edits the data '''

import sys
from decouple import config
from projects.models.paragraphs import (Group, GroupParagraph)
from common_classes.para_db_update_process import ParaDbUpdateProcess
import utilities.random_methods as utils


class ParaDbUpdateOrder(ParaDbUpdateProcess):
    '''
        ParaDbUpdateProcess updates the order of paragraphs within a group or groups within a category
        based on the order of the input.  It will overwrite the existing order.

        If a group_id is part of input: order paragraphs owned by that group
            OR (not and)
        If a category_id is part of input: order groups owned by that category

        Fail if the input data does not contain a group_id or a category_id or if it has both
        Fail if the list of paragraphs does not have an id, or text and if the count doesn't match the
            count of the paragraphs owned by the given group
        Fail if the list of groups does not have an id, or title and if the count doesn't match the
            count of the groups owned by the given category

        It is necessary to pass in both the input_data and updating (boolean)
            self.file_data = input_data.pop('file_data')
            self.script_data = input_data
            self.process_data['updating'] = updating
    '''
    RIDICULOUS = 999999999

    def __init__(self, input_data, updating):
        super().__init__(input_data, updating)
        self.group_id = self.file_data.get('group_id')
        self.category_id = self.file_data.get('category_id')
        self.process_data['parent_id'] = 0
        self.process_data['db_count'] = 0
        self.process_data['list_len'] = {}
        self.process_data['class'] = None

    def fix_order(self):
        '''
        process_input_data_update_db is the main driver of the update process.  You can see the order
        that we process the data by the method names.
        '''
        self.validations()
        self.loop_through_input_list()

    def validations(self):
        '''
        validate_input ensures that the user (me) is doing careful work

        It runs some tests on the input keys and errors with a message, if the tests fail
        '''
        if self.incorrect_environment():
            sys.exit('Input error: Update order only in the development environment')

        if self.incorrect_keys():
            sys.exit(('Input error: Keys are incorrect: '
                      f'group_id: {self.group_id}, category slug: {self.category_id}'))

        if not self.counts_work():
            sys.exit(('Input error: The counts of the input list (either groups or paras must match '
                      'the database counts for the child records to be reordered: db count=='
                      f'{self.process_data["db_count"]}, list_len=={self.process_data["list_len"]}'))
        else:
            print(('Records to update: '
                  f'{self.process_data["db_count"]}, list_len=={self.process_data["list_len"]}'))

    def incorrect_environment(self):
        if config('ENVIRONMENT') != 'development':
            return True
        return False

    def incorrect_keys(self):
        '''
            returns true if both group_id and category_id were input parameters
            but also ensures that the children keys are correct.  For example,
            groups have many paragraphs (many to many) using the group_paragraph association record
            and a category record can have many groups (one to many)
        '''
        if self.group_id and self.category_id:
            return True
        return self.incorrect_keys_based_on_owner_record()

    def incorrect_keys_based_on_owner_record(self):
        '''
            if the correct child record key and / or association record key exist
            will return False (it is truly incorrect), otherwise True (not incorrect)

            Will also be incorrect if neither a group id or a category id was passed in
        '''
        if self.group_id:
            return (utils.key_not_in_dictionary(self.file_data, 'paragraphs') and
                    utils.key_not_in_dictionary(self.file_data, 'group_paragraph'))
        if self.category_id:
            return utils.key_not_in_dictionary(self.file_data, 'groups')
        return True

    def counts_work(self):
        '''
            compares the count of the input list of paragraphs (if group_id exists) or the input list
            or groups (if category_id exists against the corresponding db counts)
        '''
        if self.group_id:
            criteria = {'group_id': self.group_id}
            self.process_data['class'] = GroupParagraph
            self.process_data['keys_to_check'] = ['paragraphs', 'group_paragraph']
            self.process_data['child_key'] = 'paragraphs'
            self.process_data['association'] = 'many_to_many'
            self.process_data['parent_id'] = self.group_id
        else:
            criteria = {'category_id': self.category_id}
            self.process_data['class'] = Group
            self.process_data['keys_to_check'] = ['groups']
            self.process_data['child_key'] = 'groups'
            self.process_data['association'] = 'one_to_many'
            self.process_data['parent_id'] = self.category_id
        self.process_data['db_count'] = self.record_counts_by_criteria(self.process_data['class'],
                                                                       **criteria)
        return self.process_data['db_count'] == self.list_lengths()

    def list_lengths(self):
        '''
            list_lengths gets the list of the input records.  These should always be correct because
            they were created programmatically, but changing the order is a manual process so must
            ensure there were no careless mistakes

        :param keys_to_check: array of keys (two for many to many associations and one for one to many)
        :type keys_to_check: list of str
        :return: 0 or ridiculously high number if results do not make sense, otherwise the list length
        :rtype: integer
        '''
        if len(self.process_data['keys_to_check']) == 1:
            return len(self.file_data[self.process_data['keys_to_check'][0]])
        if len(self.process_data['keys_to_check']) == 0:
            return self.RIDICULOUS
        for idx, key in enumerate(self.process_data['keys_to_check']):
            curr_len = len(self.file_data[key])
            if idx > 0:
                if curr_len != self.process_data['list_len'][self.process_data['keys_to_check'][idx-1]]:
                    return self.RIDICULOUS
            self.process_data['list_len'][key] = curr_len
        return curr_len

    def loop_through_input_list(self):
        '''
        loop_through_input_list loops through the list of paragraphs or groups and adds the order
        to either the cat_sort field in the group record or the groupparagraph sort field.

        It will call the create class in the base class: self.find_and_update_wrapper(key, record)
        key will either be 'groups' or 'group_paragraph'

        We will need to retrieve group_paragraph, but we will already have the group id
        '''
        for idx, ordered_rec in enumerate(self.file_data[self.process_data['child_key']]):
            order_num = idx + 1
            if self.process_data['association'] == 'many_to_many':
                self.assign_many_to_many(ordered_rec, order_num)
            else:
                self.assign_one_to_many(ordered_rec, order_num)

            returned_record = self.find_and_update_record(self.process_data['class'],
                                                          self.process_data['find_dict'],
                                                          self.process_data['update_dict'])
            if utils.key_in_dictionary(returned_record, 'error'):
                sys.exit(returned_record['error'])

    def assign_many_to_many(self, rec_dictionary, order_num):
        '''
        assign_many_to_many loops through the child records
        For many to many, however, the child record is not changed.  The association record
        defines the order of how the records are displayed

        :param rec_dictionary: one record owned by the owner record, must have the id
        :type rec_dictionary: dict
        :param order_num: The order_num to assign to the association record
        :type order_num: integer
        '''
        para_id = rec_dictionary['id']
        group_para = utils.find_dictionary_from_list_by_key_and_value(self.file_data['group_paragraph'],
                                                                      'paragraph_id',
                                                                      para_id)
        if len(group_para) != 1 and group_para[0]['group_id'] != self.group_id:
            sys.exit((f'Something got messed up: group_para has wrong group_id: para_id=={para_id}'
                      f'group_id=={self.group_id}; file_data=={self.file_data}'))
        group_para_id = group_para[0]['id']
        self.process_data['update_dict'] = {
                                                'id': group_para_id,
                                                'order': order_num
                                           }
        self.process_data['find_dict'] = {
                                            'id': group_para_id
                                         }

    def assign_one_to_many(self, rec_dictionary, order_num):
        '''
        assign_one_to_many loops through the child records and assigns the order_num
        The find_dict and create_dict are for the rec_dictionary that is passed in

        :param rec_dictionary: passed in dictionary
        :type rec_dictionary: dict
        :param order_num: The order_num to assign to the child record
        :type order_num: integer
        '''
        self.process_data['find_dict'] = {'id': rec_dictionary['id']}
        self.process_data['update_dict'] = {
                                            'id': rec_dictionary['id'],
                                            'cat_sort': order_num
                                           }
