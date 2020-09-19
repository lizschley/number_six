''' Use this for constants used strictly for crud processes '''

from projects.models.paragraphs import (Category, Group,  # noqa: F401
                                        GroupParagraph, Paragraph,
                                        ParagraphReference, Reference)

FILE_DATA = 'file_data'

VALID_RETRIEVAL_KEYS = ('updated_at', 'group_ids', 'category_ids', 'paragraph_ids')
COPY_DIRECTLY_TO_OUTPUT = ('add_categories', 'add_references', 'add_groups', 'add_paragraph_reference',
                           'add_group_paragraph', 'delete_paragraph_reference', 'delete_group_paragraph')
TABLE_ABBREV = ('c', 'g', 'p', 'r', 'gp', 'pr')


UPDATE_RECORD_KEYS = ('categories', 'references', 'paragraphs', 'groups',
                      'paragraph_reference', 'group_paragraph')

ASSOCIATION_KEYS = ('add_paragraphreference', 'add_groupparagraph',
                    'delete_paragraphreference', 'delete_groupparagraph')

CREATE_RECORD_KEYS = ('add_categories', 'add_groups', 'add_references')

CREATE_DATA = {
    'add_categories': {'unique_fields': ['title'], 'class': Category, },
    'add_references': {'unique_fields': ['link_text'], 'class': Reference, },
    'add_groups': {'unique_fields': ['title'], 'class': Group, },
    'add_paragraphs': {'unique_fields': ['guid'], 'class': Paragraph, },
    'add_groupparagraph': {'unique_fields': ['group_id', 'paragraph_id'],
                           'class': GroupParagraph, },
    'add_paragraphreference': {'unique_fields': ['paragraph_id', 'reference_id'],
                               'class': ParagraphReference, }
}

DELETE_ASSOCIATIONS = {
    'delete_groupparagraph': {'class': GroupParagraph, },
    'delete_paragraphreference': {'class': ParagraphReference, }
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
    'paragraphreference': {'paragraph': {'unique_fields': ['guid'], 'class': Paragraph},
                           'reference': {'unique_fields': ['slug'], 'class': Reference}, },
    'groupparagraph': {'group': {'unique_fields': ['slug'], 'class': Group},
                       'paragraph': {'unique_fields': ['guid'], 'class': Paragraph}, },
}
