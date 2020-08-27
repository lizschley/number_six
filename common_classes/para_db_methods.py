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

    def create_record(self, class_, create_dict):
        record = class_(**create_dict)
        if self.updating:
            record.save()
        else:
            return create_dict
        print(f'created record {record}')
        return record

    def find_record(self, class_, find_dict):
        return class_.objects.get(**find_dict)

    @staticmethod
    def class_based_rawsql_retrieval(sql, class_, *args):
        '''
        class_based_rawsql_retrieval highly reusable retrieval query
        :param sql: arguments with the key matching the key in the query
        :type sql: str
        :param class_: class to start with
        :type class_: model class
        :return: result from query
        :rtype: rawsql queryset
        '''
        return class_.objects.raw(sql, [args])

