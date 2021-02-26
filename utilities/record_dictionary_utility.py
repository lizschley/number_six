'''Utility for creating static resusable methods to use in the batch update process'''
# pylint: pylint: disable=unused-import
import sys
import constants.crud as crud
import utilities.json_methods as json_helper
from projects.models.paragraphs import (Category, Reference, Paragraph, Group,  # noqa: F401
                                        GroupParagraph, ParagraphReference)  # noqa: F401


class RecordDictionaryUtility:
    '''
    RecordDictionaryUtility contains static methods to easily create dictionaries to be used to
    update existing records.

    See scripts/db_updater_s1.py and scripts/updater_s3.py for more details

    It is used to create the methods in helpers.no_import_common_class.paragraph_dictionaries

    :param object: inherits from object
    :type object: Object object
    '''
    @staticmethod
    def create_json_list_of_records(out_dir, input_data):
        ''' list db record data in json file; records retrieved based on input parameters '''
        key = input_data['params']['key']
        class_ = crud.UPDATE_DATA[key]['class']
        id_list = RecordDictionaryUtility.retrieve_id_list(class_,
                                                           input_data['params']['select_criteria'])
        out_directory = {'directory_path': out_dir}
        dict_output = RecordDictionaryUtility.create_output(key, class_, id_list)
        json_helper.write_dictionary_to_file(dict_output, **out_directory)

    @staticmethod
    def create_output(key, class_, id_list):
        ''' used to get dictionary representation of db records using list of ids '''
        dict_output = {key: []}
        for pk_id in id_list:
            queryset = RecordDictionaryUtility.get_content(class_, pk_id=pk_id)
            dict_output[key].append(queryset[0])
        return dict_output

    @staticmethod
    def retrieve_id_list(class_, criteria):
        ''' get list of ids based on input parameters '''
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
        ''' retrieve list of all the ids for a given model '''
        id_list = []
        queryset = class_.objects.values_list('id')
        for qs in queryset:
            id_list.append(qs[0])
        return id_list


    # Just pass in the model class name and id if id #1 has been deleted
    @staticmethod
    def get_content(class_, pk_id=1):
        ''' time saver in creating content for paragraph dictionaries '''
        return class_.objects.filter(id=pk_id).values()
