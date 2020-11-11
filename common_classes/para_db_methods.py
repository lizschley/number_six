'''These will be static resusable methods to create &/or update records'''
# pylint: pylint: disable=unused-import
import sys
from django.core.exceptions import ValidationError
from django.utils import timezone
import helpers.no_import_common_class.utilities as utils
from projects.models.paragraphs import (Category, Reference, Paragraph, Group,  # noqa: F401
                                        GroupParagraph, ParagraphReference)  # noqa: F401
from utilities.record_dictionary_utility import RecordDictionaryUtility


class ParaDbMethods:
    '''
    ParagraphsRecordCreateOrUpdate is a class of static methods to retrieve, update or create
    paragraph associated records.

    :param object: inherits from object
    :type object: Object object
    '''

    def __init__(self, updating):
        self.updating = updating

    def find_or_create_record(self, class_, find_dict, create_dict):
        '''
        find_or_create_record will look for the record using the unique field in find_dict. If it
        does not exist, the record will be created
        :return: dictionary including the record found or created
        :rtype: dict or model.Model
        '''
        found = True
        try:
            record = class_.objects.get(**find_dict)
            return {'found': found, 'record': record}
        except class_.DoesNotExist:
            found = False
            if self.updating:
                self.create_record(class_, create_dict)
            else:
                return {'found': found, 'record': create_dict}
        return {'found': found, 'record': class_.objects.get(**find_dict)}

    def find_and_update_record(self, class_, find_dict, update_dict):
        '''
        find_or_update_record will look for the record using the unique field in find_dict. If it
        if found, it will check the id.  If that is not the same, it will pass back an error message,
        which will be dealt with in the calling program

        If the record is a paragraph, it will validate it before calling the update method.  If the
        paragraph does not pass the validation, it will return an error message (a dict)

        :return: dictionary of newly updated record or the record that was found (if not updating)
        :rtype: dict
        '''
        try:
            record = class_.objects.get(**find_dict)
        except class_.DoesNotExist:
            return {'error': f'{class_.__name__} with unique key {find_dict} does not exist.'}

        results = ParaDbMethods.valid_paragraph_subtitle(record, update_dict)
        if not results['valid']:
            return {'error': f'Invalid paragraph! {results["message"]}'}

        if update_dict['id'] == record.id:
            update_dict['updated_at'] = timezone.now()
            self.update_record(class_, update_dict)
        else:
            print('Error! The found record id does not match the input record, existing without update.')
            print(f'input=={update_dict}, and found== {record}')
        queryset = RecordDictionaryUtility.get_content(class_, pk_id=record.id)
        return queryset[0]

    @staticmethod
    def valid_paragraph_subtitle(para, update_dict):
        '''
        valid_paragraph_subtitle checks to ensure that standalone paragraphs do not have blank or
        non-unique subtitles.  Non-standalone paragraphs are ok either way (technically at least)

        :param para: This is a dictionary form of the paragraph before it is updated.
        :type para: Paragraph (program will send in other models, but the method checks)
        :param update_dict: id, unique_key and fields to be changed
        :type update_dict: dictionary
        :return: dictionary with valid key that is true or False.  If False, will have error message
        :rtype: dict
        '''
        if not isinstance(para, Paragraph):
            # ret = {'valid': True}
            return {'valid': True}
        if utils.key_in_dictionary(update_dict, 'standalone'):
            # print(f'if #2, updating para.standalone to {update_dict["standalone"]}')
            para.standalone = update_dict['standalone']
        if not para.standalone:
            # ret = {'valid': True}
            # print(f'if #3 returning {ret}')
            return {'valid': True}
        if utils.key_in_dictionary(update_dict, 'subtitle'):
            # print(f'if 4, updating para.subtitle to {update_dict["subtitle"]}')
            para.subtitle = update_dict['subtitle']
        if not para.subtitle.strip():
            # ret = {'valid': False, 'message': f'Empty subtitle on standalone para: {para}'}
            # print(f'if #5 returning {ret}')
            return {'valid': False, 'message': f'Empty subtitle on standalone para: {para}'}
        if Paragraph.objects.exclude(guid=para.guid).filter(subtitle__iexact=para.subtitle).exists():
            # ret = {'valid': False, 'message': f'Not unique subtitle for para: {para}'}
            # print(f'if 6, found an identical subtitle in another para, ret=={ret}')
            return {'valid': False, 'message': f'Not unique subtitle for para: {para}'}
        # ret = {'valid': True}
        # print('passed all the tests, therefore valid, ret=={ret}')
        return {'valid': True}

    def update_record(self, class_, update_dict):
        '''
        update_record takes the model class name and the dictionary for updating

        :param class_: model class
        :type class_: models.Model
        :param update_dict: Dictionary with the id and the fields to update
        :type update_dict: dict
        '''
        if not self.updating:
            return
        pk_id = update_dict.pop('id')
        class_.objects.filter(pk=pk_id).update(**update_dict)

    # Todo: Check return type, print statements already in
    def create_record(self, class_, create_dict):
        '''
        create_record - creates a record of the class type with the values in create_dict

        May throw ValidationError

        :param class_: Model name, for example: Group
        :type class_: Model object
        :param create_dict: values for fields for given model
        :type create_dict: dict
        :return: object created model class, where the class_ is django model instance
        :rtype: projects.models.paragraphs.ClassName instance
        '''
        record = class_(**create_dict)
        if not self.updating:
            return record
        try:
            record.full_clean()
        except ValidationError:
            print(f'got validation error: {record}')
            raise
        record.save()
        return record

    def find_record(self, class_, find_dict):
        '''
        find_record on the field defined in find_dict

        :param class_: Model name, for example: Group
        :type class_: Model object
        :param find_dict: dictionary with field and values used to find the given model's record
        :type find_dict: dict
        :return: queryset - containing instance of given model (could be list, depending on find_dict)
        :rtype: queryset
        '''
        try:
            return_obj = class_.objects.get(**find_dict)
        except class_.DoesNotExist:
            if self.updating:
                raise
            return_obj = find_dict
        return return_obj

    # Todo: Haven't written test for this yet
    def delete_record(self, class_, find_dict):
        '''
        delete_record deletes the records found using filter

        :param class_: Model for the record you want deleted
        :type class_: models.Model
        :param find_dict: dictionary with the unique key
        :type find_dict: dict
        '''
        if class_ not in (GroupParagraph, ParagraphReference):
            sys.exit(f'Not allowing hard deletes of {class_.__name__}')
        if self.updating:
            class_.objects.filter(**find_dict).delete()

    @staticmethod
    def class_based_rawsql_retrieval(sql, class_, *args):
        '''
        class_based_rawsql_retrieval reusable retrieval query
        :param sql: arguments with the key matching the key in the query
        :type sql: str
        :param class_: class to start with
        :type class_: model class
        :return: result from query
        :rtype: rawsql queryset
        '''
        return class_.objects.raw(sql, [args])
