select g.title, left(p.text, 25) as beg_para, g.slug, g.id as group_id, p.guid, p.id as para_id
from projects_group g
join projects_groupparagraph gp on g.id = gp.group_id
join projects_paragraph p on p.id = gp.paragraph_id
where g.category_id = 1
order by p.id

select string_agg(distinct cast (p.id as varchar), ',') as para_ids
from projects_group g
join projects_groupparagraph gp on g.id = gp.group_id
join projects_paragraph p on p.id = gp.paragraph_id
where g.category_id = 1 and p.id > 118
