'''These will be static resusable methods to create &/or update records'''
# pylint: pylint: disable=unused-import
from projects.models.paragraphs import (Category, Reference, Paragraph, Group,  # noqa: F401
                                        GroupParagraph, ParagraphReference)  # noqa: F401


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
        find_or_create_group will look for a group using the title, which must be unique.  It it
        does not exist, it will be created
        :return: string that says ok or an error message (may change later)
        :rtype: [type]
        '''
        try:
            # group = Group.objects.get(title=find_dict['title'])
            record = class_.objects.get(**find_dict)
        except class_.DoesNotExist:
            record = class_(**create_dict)
            if self.updating:
                record.save()
            else:
                return create_dict
            record = class_.objects.get(**find_dict)
        return record

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
