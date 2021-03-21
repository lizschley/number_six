'''These will be static resusable methods to use in the batch update process'''
import sys
import uuid
from django.utils.text import slugify


class ParagraphDictionaries:
    '''
    ParagraphDictionaries is a class of static methods to easily create dictionaries to be used to update
    existing records.

    Returns an empty dictionary to use when in Step 1 & input to Step 2 of batch updater+

    See scripts/db_updater_s1.py and scripts/batch_json_db_updater_s2.py for more details

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
            'short_text': '',
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
            'slug': '',
            'short_title': '',
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

    @staticmethod
    def group_para_associations(guid, slugs):
        '''
        group_para_associations returns a dictionary needed to add or delete GroupParagraph associations

        :param input: dictionary with these keys: guid, group_slug
        :type input: dict
        :return: dictioary with the exact format needed to add or delete group para associations
        :rtype: dict
        '''
        association_list = []
        group_list = slugs.split(',')
        for slug in group_list:
            if len(slug.strip()) == 0:
                continue
            association = {'group_slug': slug.strip(), 'paragraph_guid': guid.strip()}
            association_list.append(association)
        return association_list

    @staticmethod
    def add_unique_field(record, key, unique_field):
        '''
            add_unique_field makes it possible to explicitly add unique fields to the paragraph records.
            Not currently using this, but it has been created and tested back when it was needed and
            there are ways to use it for sure.

            :param record: dictionary that corresponds to one of the four main paragraph records
            :type record: dict
            :param key: key used to find the information necessary to run generic creates and updates
            :type key: str
            :param unique_field: key that is used to identify records, always unique for given db table
            :type unique_field: str
            :return: dictionary with necessary information to create a new record
            :rtype: dict
        '''
        if key == 'references':
            record[unique_field] = slugify(record['link_text'])
        elif key == 'paragraphs':
            record[unique_field] = str(uuid.uuid4())
        elif key in ('categories', 'groups'):
            record[unique_field] = slugify(record['title'])
        else:
            sys.exit(f'Error! Invalid key in add_unique_field, key == {key} & record == {record}')
        return record

    @staticmethod
    def text_only_paragraph_updates(guid, pk_id, text):
        ''' use this for updates to text field only when editing programmaically '''
        return {
            'guid': guid,
            'id': pk_id,
            'text': text,
        }

