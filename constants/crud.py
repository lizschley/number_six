''' Use this for constants used strictly for crud processes '''

from projects.models.paragraphs import (Category, Group,  # noqa: F401
                                        GroupParagraph, Paragraph,
                                        ParagraphReference, Reference)

FILE_DATA = 'file_data'

VALID_RETRIEVAL_KEYS = ('updated_at', 'group_ids', 'category_ids', 'paragraph_ids', 'reference_ids')
COPY_DIRECTLY_TO_OUTPUT = ('add_categories', 'add_references', 'add_groups', 'add_paragraph_reference',
                           'add_group_paragraph', 'delete_paragraph_reference', 'delete_group_paragraph')
TABLE_ABBREV = ('c', 'g', 'p', 'r', 'gp', 'pr')

# The order of these records is important, because earlier records may have primary keys that are used
# as foreign keys in later records
UPDATE_RECORD_KEYS = ('categories', 'references', 'paragraphs', 'groups',
                      'paragraph_reference', 'group_paragraph')

ASSOCIATION_RECORD_KEYS = ('paragraph_reference', 'group_paragraph')

ASSOCIATION_KEYS = ('add_paragraph_reference', 'add_group_paragraph',
                    'delete_paragraph_reference', 'delete_group_paragraph')

CREATE_RECORD_KEYS = ('add_categories', 'add_groups', 'add_references')

CREATE_DATA = {
    'add_categories': {'unique_fields': ['title'], 'class': Category, },
    'add_references': {'unique_fields': ['link_text'], 'class': Reference, },
    'add_groups': {'unique_fields': ['title'], 'class': Group, },
    'add_paragraphs': {'unique_fields': ['guid'], 'class': Paragraph, },
    'add_group_paragraph': {'unique_fields': ['group_id', 'paragraph_id'],
                            'class': GroupParagraph, },
    'add_paragraph_reference': {'unique_fields': ['paragraph_id', 'reference_id'],
                                'class': ParagraphReference, }
}

DELETE_KEYS = ('delete_paragraph_reference', 'delete_group_paragraph')

DELETE_ASSOCIATIONS = {
    'delete_group_paragraph': {'class': GroupParagraph, },
    'delete_paragraph_reference': {'class': ParagraphReference, }
}

UPDATE_DATA = {
    'categories': {'unique_field': 'slug', 'class': Category},
    'references': {'unique_field': 'slug', 'class': Reference},
    'paragraphs': {'unique_field': 'guid', 'class': Paragraph},
    'groups': {'unique_field': 'slug', 'class': Group},
    'paragraph_reference': {'unique_field': 'id', 'class': ParagraphReference},
    'group_paragraph': {'unique_field': 'id', 'class': GroupParagraph}
}

ASSOCIATION_DATA = {
    'paragraph_reference': {'paragraph': {'unique_fields': ['guid'], 'class': Paragraph},
                            'reference': {'unique_fields': ['slug'], 'class': Reference}, },
    'group_paragraph': {'group': {'unique_fields': ['slug'], 'class': Group},
                        'paragraph': {'unique_fields': ['guid'], 'class': Paragraph}, },
}

RECORD_LOOKUP_MESSAGE = ('Input Error!  Please read documentation!  Must run Step One with the '
                         'for_prod script argument. ')
RECORD_LOOKUP_MESSAGE_PROD = RECORD_LOOKUP_MESSAGE + ('Since this is production, editing could mess up '
                                                      'the entire process.')
RECORD_LOOKUP_MESSAGE_DEV = RECORD_LOOKUP_MESSAGE + ('In development, you should edit the data, but do '
                                                     'not use this method unless you know what you are '
                                                     'doing.')

UPDATE_ASSOCIATED = ('group_paragraph')

PARA_ID_REF_LINK_TEXT = {
    'key_1': 'paragraph_id',
    'para_val_1_key': 'id',
    'key_2': 'link_text',
    'para_val_2_key': 'link_text_list',
}

PARA_GUID_REF_LINK_TEXT = {
    'key_1': 'paragraph_guid',
    'para_val_1_key': 'guid',
    'key_2': 'link_text',
    'para_val_2_key': 'link_text_list',
}

PARA_GUID_REF_SLUG = {
    'key_1': 'paragraph_guid',
    'para_val_1_key': 'guid',
    'key_2': 'reference_slug',
    'para_val_2_key': 'ref_slug_list',
}
