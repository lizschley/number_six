select slug, text
from projects_paragraph p
join projects_groupparagraph gp on p.id = gp.paragraph_id
where gp.group_id = 3 and text like '%|beg%'
