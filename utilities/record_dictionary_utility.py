'''Utility for creating static resusable methods to use in the batch update process'''
# pylint: pylint: disable=unused-import
import datetime
import json
import sys
import constants.crud as crud
from common_classes.paragraph_db_input_creator import ParagraphDbInputCreator
from projects.models.paragraphs import (Category, Reference, Paragraph, Group,  # noqa: F401
                                        GroupParagraph, ParagraphReference)  # noqa: F401
import utilities.date_time as utils


class RecordDictionaryUtility:
    '''
    RecordDictionaryUtility contains static methods to easily create dictionaries to be used to
    update existing records.

    See scripts/batch_json_db_updater_s1.py and scripts/batch_json_db_updater_s2.py for more details

    It is used to create the methods in helpers.no_import_common_class.paragraph_dictionaries

    :param object: inherits from object
    :type object: Object object
    '''
    @staticmethod
    def create_json_list_of_records(out_dir, input_data):
        key = input_data['params']['key']
        class_ = crud.UPDATE_DATA[key]['class']
        id_list = RecordDictionaryUtility.retrieve_id_list(class_,
                                                           input_data['params']['select_criteria'])
        out_directory = {'directory_path': out_dir}
        dict_output = RecordDictionaryUtility.create_output(key, class_, id_list)
        RecordDictionaryUtility.write_dictionary_to_file(dict_output, **out_directory)

    @staticmethod
    def create_output(key, class_, id_list):
        dict_output = {key: []}
        for pk_id in id_list:
            queryset = RecordDictionaryUtility.get_content(class_, pk_id=pk_id)
            dict_output[key].append(queryset[0])
        print(f'dict_output == {dict_output}')
        return dict_output

    @staticmethod
    def retrieve_id_list(class_, criteria):
        if criteria == 'all':
            return RecordDictionaryUtility.retrieve_id_list_from_all(class_)
        id_list = []
        string_list = criteria.split(',')
        for str_id in string_list:
            try:
                int_id = str(str_id)
            except ValueError:
                sys.exit(f'Error! Invalid argument, expected "all" or "2,3,4"; got {string_list}')
            id_list.append(int_id)
        return id_list

    @staticmethod
    def retrieve_id_list_from_all(class_):
        id_list = []
        queryset = class_.objects.values_list('id')
        for qs in queryset:
            id_list.append(qs[0])
        return id_list

    @staticmethod
    def write_dictionary_to_file(output_data, **kwargs):
        '''
        write_dictionary_to_file is a static method that can be used generically, though it does take
        advantage of some of the batch json db update processing

        Key word args are optional:
        prefix will be input_, unless you override
        filename will be prefix_datetime.json unless you override (note = won't use prefix if you provide
                 filename)
        directory_path will be base path + data/data_for_creates unless you override

        :param input_data: dictionary to be written to json
        :type input_data: dictionary
        '''
        output_file = open(ParagraphDbInputCreator.create_json_file_path(**kwargs), 'w')
        # magic happens here to make it pretty-printed
        output_file.write(json.dumps(output_data, default=utils.postgres_friendly_datetime,
                                     indent=4, sort_keys=True))
        output_file.close()

    # Just pass in the model class name and id if id #1 has been deleted
    @staticmethod
    def get_content(class_, pk_id=1):
        ''' time saver in creating content for paragraph dictionaries '''
        return class_.objects.filter(id=pk_id).values()
