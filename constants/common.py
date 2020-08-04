'''These are constants that will be used either for validation, processing or both'''
EXCLUDE_GROUP_FROM_STUDY = ['Chronological Resume', 'Functional Resume', 'Native Plant Blog',
                            'Web Application Blog']
ORDER_FIELD_FOR_PARAS = 'order'
VALID_DATA_RETRIEVAL_ARGS = ('group_id', 'path_to_json', 'subtitle')
VALID_DB_RETRIEVER_KW_ARGS = ('group_id', 'search_str', 'subtitle')
SUBTITLE = 'subtitle'

BEGIN_SELECT = 'select 1 as id'
SELECT_GROUP = 'g.id as group_id, title as title, g.note as title_note, gp.order'
SELECT_PARAGRAPHS = ('p.id as paragraph_id, subtitle, p.note as subtitle_note, image_path, '
                     'image_info_key, text')
SELECT_REFERENCES = 'r.id as reference_id, link_text, url'

FROM_GROUP_JOIN_PARA = ('from projects_group g '
                        'join projects_groupparagraph gp on g.id = gp.group_id '
                        'join projects_paragraph p on p.id = gp.paragraph_id ')
FROM_PARA = 'from projects_paragraph p'

JOIN_REFERENCES_TO_PARA = ('join projects_paragraphreference pr on p.id = pr.paragraph_id '
                           'join projects_reference r on r.id = pr.reference_id ')
