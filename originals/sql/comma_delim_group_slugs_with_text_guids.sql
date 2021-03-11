select p.guid, p.text, string_agg(g.slug, ', ') as group_slugs
from projects_paragraph p
join projects_groupparagraph gp on gp.paragraph_id = p.id
join projects_group g on g.id = gp.group_id
where g.category_id = 1
group by p.guid, p.text
