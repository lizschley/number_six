'''These will be static resusable methods to use in the batch update process'''
# pylint: pylint: disable=unused-import
# pylint: disable=missing-function-docstring

from projects.models.paragraphs import (Category, Reference, Paragraph, Group,  # noqa: F401
                                        GroupParagraph, ParagraphReference)  # noqa: F401


class ParagraphDictionaries:
    '''
    ParagraphDictionaries is a class of static methods to easily create dictionaries to be used to update
    existing records.

    See scripts/batch_json_db_updater_s1.py and scripts/batch_json_db_updater_s2.py for more details

    There are two groups of methods:
       First - empty dictionaries used for creating output in Step 1 & input to Step 2 of batch updater
       Second (just one method) - content_creator utility, this is to save me time and effort only

    :param object: inherits from object
    :type object: Object object
    '''

    # First group below:
    # empty dictionaries used for creating output in Step 1 & input to Step 2 of batch updater
    # Todo: do category when there acutally is one
    @staticmethod
    def category_dictionary():
        return {}

    @staticmethod
    def reference_dictionary():
        return {
            'id': 0,
            'link_text': '',
            'slug': '',
            'url': '',
        }

    @staticmethod
    def paragraph_dictionary():
        return {
            'id': 0,
            'subtitle': '',
            'note': '',
            'text': '',
            'standalone': True,
            'image_path': '',
            'image_info_key': 'default',
            'guid': '',
        }

    @staticmethod
    def group_dictionary():
        return {
            'id': 0,
            'title': '',
            'slug': '',
            'note': '',
            'category_id': None,
        }

    @staticmethod
    def groupparagraph_dictionary():
        return {
            'id': 0,
            'group_id': 0,
            'paragraph_id': 0,
            'order': 0,
        }

    @staticmethod
    def paragraphreference_dictionary():
        return {
            'id': 0,
            'reference_id': 0,
            'paragraph_id': 0,
        }

    # Second group only one actually:
    # Just pass in the model name and id if one is no good
    @staticmethod
    def get_content(class_, id_to_use=1):
        return class_.objects.filter(id=id_to_use).values()
