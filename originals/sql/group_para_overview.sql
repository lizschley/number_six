select g.category_id, g.id as g_id, p.slug as para_slug, g.slug as group_slug, gp.order, left(p.text, 120) as beg_para, p.id as para_id
from projects_paragraph p
join projects_groupparagraph gp on p.id = gp.paragraph_id
join projects_group g on g.id = gp.group_id
where p.updated_at >= '2021-04-04'
order by g.id, gp.order

