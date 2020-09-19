'''Utility for creating static resusable methods to use in the batch update process'''
# pylint: pylint: disable=unused-import


from projects.models.paragraphs import (Category, Reference, Paragraph, Group,  # noqa: F401
                                        GroupParagraph, ParagraphReference)  # noqa: F401


class ParagraphDictionaryUtility:
    '''
    ParagraphDictionaryUtility contains a static methods to easily create dictionaries to be used to
    update existing records.

    See scripts/batch_json_db_updater_s1.py and scripts/batch_json_db_updater_s2.py for more details

    It is used to create the methods in helpers.no_import_common_class.paragraph_dictionaries

    :param object: inherits from object
    :type object: Object object
    '''

    # Just pass in the model class name and id if id #1 has been deleted
    @staticmethod
    def get_content(class_, id_to_use=1):
        ''' time saver in creating content for paragraph dictionaries '''
        return class_.objects.filter(id=id_to_use).values()
