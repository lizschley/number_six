''' Use to build sql '''
BEGIN_SELECT = 'select 1 as id'
SELECT_CATEGORY = ('c.id as category_id, c.title as category_title, c.slug as category_slug, '
                   'c.category_type as category_type ')
SELECT_GROUP = ('g.id as group_id, g.short_name as group_short_name, g.title as group_title, '
                'g.group_type as group_type, g.note as group_note, g.cat_sort as cat_sort, gp.order, '
                'g.slug as group_slug ')
SELECT_PARAGRAPHS = ('p.id as paragraph_id, subtitle, p.note as subtitle_note, image_path, '
                     'image_info_key, text, p.slug as para_slug')
SELECT_REFERENCES = 'r.id as reference_id, link_text, url, short_text, r.slug as ref_slug '

FROM_CATEGORY_JOIN_GROUP_AND_PARA = ('from projects_category c '
                                     'join projects_group g on c.id = g.category_id '
                                     'join projects_groupparagraph gp on g.id = gp.group_id '
                                     'join projects_paragraph p on p.id = gp.paragraph_id ')

FROM_GROUP_JOIN_PARA = ('from projects_group g '
                        'join projects_groupparagraph gp on g.id = gp.group_id '
                        'join projects_paragraph p on p.id = gp.paragraph_id ')

FROM_PARA = 'from projects_paragraph p '

JOIN_GROUP_TO_PARA = ('join projects_groupparagraph gp on p.id = gp.paragraph_id '
                      'join projects_group g on g.id = gp.group_id ')

JOIN_CATEGORY_TO_GROUP = ('left outer join projects_category c on c.id = g.category_id ')

JOIN_REFERENCES_TO_PARA = ('left outer join projects_paragraphreference pr on p.id = pr.paragraph_id '
                           'left outer join projects_reference r on r.id = pr.reference_id ')

# the following are for updates, which may be creates in production
COMPLETE_CATEGORY_SELECT = ('c.id as category_id, c.title as category_title, c.slug as category_slug, '
                            'c.category_type, c.created_at as category_created_at, '
                            'c.updated_at as category_updated_at ')

COMPLETE_GP_SELECT = ('gp.id as gp_id, gp.group_id as gp_group_id, gp.paragraph_id as gp_para_id, '
                      'gp.order as gp_order, gp.created_at as gp_created_at, '
                      'gp.updated_at as gp_updated_at ')


COMPLETE_GROUP_SELECT = ('g.id as group_id, g.category_id as group_category_id, g.title as group_title, '
                         'g.slug as group_slug, g.note as group_note, g.created_at as group_created_at, '
                         'g.updated_at as group_updated_at, g.short_name as group_short_name, '
                         'g.cat_sort as cat_sort, g.group_type as group_type')

COMPLETE_PR_SELECT = ('pr.id as pr_id, pr.paragraph_id as pr_para_id, '
                      'pr.reference_id as pr_reference_id, pr.created_at as pr_created_at, '
                      'pr.updated_at as pr_updated_at ')

COMPLETE_PARAGRAPH_SELECT = ('p.id as para_id, p.guid as para_guid, '
                             'p.subtitle as para_subtitle, p.note as para_note,'
                             'p.text as para_text, p.image_info_key as para_image_info_key, '
                             'p.image_path as para_image_path, p.standalone as para_standalone, '
                             'p.created_at as para_created_at, p.updated_at as para_updated_at, '
                             'p.slug  as para_slug')

COMPLETE_REFERENCE_SELECT = ('r.id as reference_id, r.link_text as reference_link_text, '
                             'r.slug as reference_slug, r.url as reference_url, '
                             'r.short_text as short_text, r.created_at as reference_created_at, '
                             'r.updated_at as reference_updated_at ')

CATEGORY_SORT = 'order by g.cat_sort, gp.order'
