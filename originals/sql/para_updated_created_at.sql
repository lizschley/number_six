select p.updated_at, p.created_at, p.subtitle, left(p.text, 120) as beg_para, p.id as para_id
from projects_paragraph p
join projects_groupparagraph gp on p.id = gp.paragraph_id
where gp.group_id = 9
order by p.subtitle desc

