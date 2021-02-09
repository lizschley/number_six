select
   1 as id,
   c.id as category_id,
   c.title as category_title,
   c.slug as category_slug,
   c.category_type,
   c.created_at as category_created_at,
   c.updated_at as category_updated_at,
   gp.id as gp_id,
   gp.group_id as gp_group_id,
   gp.paragraph_id as gp_para_id,
   gp.order as gp_order,
   gp.created_at as gp_created_at,
   gp.updated_at as gp_updated_at,
   g.id as group_id,
   g.category_id as group_category_id,
   g.title as group_title,
   g.slug as group_slug,
   g.note as group_note,
   g.created_at as group_created_at,
   g.updated_at as group_updated_at,
   pr.id as pr_id,
   pr.paragraph_id as pr_para_id,
   pr.reference_id as pr_reference_id,
   pr.created_at as pr_created_at,
   pr.updated_at as pr_updated_at,
   p.id as para_id,
   p.guid as para_guid,
   p.subtitle as para_subtitle,
   p.note as para_note,
   p.text as para_text,
   p.image_info_key as para_image_info_key,
   p.image_path as para_image_path,
   p.standalone as para_standalone,
   p.created_at as para_created_at,
   p.updated_at as para_updated_at,
   r.id as reference_id,
   r.link_text as reference_link_text,
   r.slug as reference_slug,
   r.url as reference_url,
   r.created_at as reference_created_at,
   r.updated_at as reference_updated_at
from
   projects_paragraph p
   join
      projects_groupparagraph gp
      on p.id = gp.paragraph_id
   join
      projects_group g
      on g.id = gp.group_id
   left outer join
      projects_category c
      on c.id = g.category_id
   left outer join
      projects_paragraphreference pr
      on p.id = pr.paragraph_id
   left outer join
      projects_reference r
      on r.id = pr.reference_id
where
   c.updated_at >= '2020-09-09 18:34:53+00'
   or g.updated_at >= '2020-09-09 18:34:53+00'
   or p.updated_at >= '2020-09-09 18:34:53+00'
   or r.updated_at >= '2020-09-09 18:34:53+00'
   or gp.updated_at >= '2020-09-09 18:34:53+00'
   or pr.updated_at >= '2020-09-09 18:34:53+00'
