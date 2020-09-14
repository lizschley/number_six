'''These will be static resusable methods to create &/or update records'''
# pylint: pylint: disable=unused-import
import sys
from django.utils import timezone
from projects.models.paragraphs import (Category, Reference, Paragraph, Group,  # noqa: F401
                                        GroupParagraph, ParagraphReference)  # noqa: F401
from utilities.paragraph_dictionaries import ParagraphDictionaries


class ParaDbMethods:
    '''
    ParagraphsRecordCreateOrUpdate is a class of static methods to retrieve, update or create
    paragraph associated records.

    :param object: inherits from object
    :type object: Object object
    '''

    def __init__(self, updating):
        self.updating = updating

    # Todo: Check type
    def find_or_create_record(self, class_, find_dict, create_dict):
        '''
        find_or_create_record will look for the record using the unique field in find_dict. If it
        does not exist, the record will be created
        :return: the record created or found
        :rtype: [type]
        '''
        try:
            return class_.objects.get(**find_dict)
        except class_.DoesNotExist:
            record = class_(**create_dict)
            if self.updating:
                record.save()
            else:
                return create_dict
        return class_.objects.get(**find_dict)

    def find_and_update_record(self, class_, find_dict, update_dict):
        '''
        find_or_update_record will look for the record using the unique field in find_dict. If it
        if found, it will check the id.  If that is not the same, it will pass back an error message,
        which will be dealt with in the calling program

        :return: string that says ok or an error message (may change later)
        :rtype: [type]
        '''
        try:
            record = class_.objects.get(**find_dict)
        except class_.DoesNotExist:
            return {'error': f'{class_.__name__} with unique key {find_dict} does not exist.'}
        if update_dict['id'] == record.id:
            update_dict['updated_at'] = timezone.now()
            self.update_record(class_, update_dict)
        queryset = ParagraphDictionaries.get_content(class_, id_to_use=record.id)
        return queryset[0]

    def update_record(self, class_, update_dict):
        '''
        update_record send in the model class name and the dictionary for updating

        :param class_: model class
        :type class_: models.Model
        :param update_dict: Dictionary with the id and the fields to update
        :type update_dict: dict
        '''
        if self.updating:
            pk_id = update_dict.pop('id')
            print(f'Doing {class_.__name__} update!!')
            class_.objects.filter(pk=pk_id).update(**update_dict)

    # Todo: Check type
    def create_record(self, class_, create_dict):
        '''
        create_record - creates a record of the class type with the values in create_dict

        :param class_: Model name, for example: Group
        :type class_: Model object
        :param create_dict: values for fields for given model
        :type create_dict: dict
        :return: object created
        :rtype: queryset or object
        '''
        record = class_(**create_dict)
        if self.updating:
            record.save()
        else:
            return record
        print(f'created record {record}')
        return record

    def find_record(self, class_, find_dict):
        '''
        find_record on the field defined in find_dict

        :param class_: Model name, for example: Group
        :type class_: Model object
        :param find_dict: dictionary with field and values used to find the given model's record
        :type find_dict: dict
        :return: queryset - instance of given model
        :rtype: queryset
        '''
        return class_.objects.get(**find_dict)

    # Todo: Test this manually and later programmatically
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
        print(f'deleting {find_dict} in {class_.__name__}')
        if self.updating:
            class_.objects.filter(**find_dict).delete()
        else:
            print(f'deleting {class_.objects.filter(**find_dict)}')

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
