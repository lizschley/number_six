'''These will be static resusable methods to use in the batch update process'''


class ParagraphDictionaries:
    '''
    ParagraphDictionaries is a class of static methods to easily create dictionaries to be used to update
    existing records.

    Returns an empty dictionary to use when in Step 1 & input to Step 2 of batch updater+

    See scripts/batch_json_db_updater_s1.py and scripts/batch_json_db_updater_s2.py for more details

    There is a sister class, utilities.record_dictionary_utility (RecordDictionaryUtility) that has
    a method to save time and effort in creating or updating these classes

    :param object: inherits from object
    :type object: Object object
    '''

    # First group below:
    # empty dictionaries used for creating output in Step 1 & input to Step 2 of batch updater
    @staticmethod
    def category_dictionary():
        ''' returns empty category dictionary '''
        return {'id': 0,
                'title': '',
                'slug': '',
                'category_type': '',
                }

    @staticmethod
    def reference_dictionary():
        ''' returns empty reference dictionary '''
        return {
            'id': 0,
            'link_text': '',
            'slug': '',
            'url': '',
        }

    @staticmethod
    def paragraph_dictionary():
        ''' returns empty paragraph dictionary '''
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
        ''' returns empty group dictionary '''
        return {
            'id': 0,
            'title': '',
            'slug': '',
            'note': '',
            'category_id': 0,
            'short_name': '',
            'cat_sort': 0,
            'group_type': '',
        }

    @staticmethod
    def groupparagraph_dictionary():
        ''' returns empty groupparagraph dictionary '''
        return {
            'id': 0,
            'group_id': 0,
            'paragraph_id': 0,
            'order': 0,
        }

    @staticmethod
    def paragraphreference_dictionary():
        ''' returns empty paragraphreference dictionary '''
        return {
            'id': 0,
            'reference_id': 0,
            'paragraph_id': 0,
        }

    @staticmethod
    def reference_link_data(row):
        '''
        reference_link_data returns the reference data needed to create various kinds of links

        :param row: is one row from a sql query
        :type row: partial query set
        :return: data needed to create links to display
        :rtype: dict
        '''
        return {'link_text': row.link_text, 'url': row.url,
                'short_text': row.short_text, 'slug': row.ref_slug}
