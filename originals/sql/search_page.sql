select 
  1 as id, 
  g.id as group_id, 
  g.group_type, 
  g.slug, 
  g.short_name as group_link_text, 
  p.id as para_id, 
  p.standalone, 
  p.slug as para_slug, 
  p.short_title as para_link_text 
from 
  projects_group g 
  join projects_groupparagraph gp on g.id = gp.group_id 
  join projects_paragraph p on p.id = gp.paragraph_id 
  left outer join projects_category c on c.id = g.category_id 
where 
  c.category_type not in ('archived', 'resume') 
  and group_type <> 'no_search' 
  and (
    g.title like '%blue%' 
    or p.subtitle like '%blue%' 
    or p.text like '%blue%'
  ) 
order by 
  g.group_type, 
  p.subtitle
