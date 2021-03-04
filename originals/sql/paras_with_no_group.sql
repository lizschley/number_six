select p.guid, p.id as para_id, left(p.text, 100) as beg_para, gp.group_id
from projects_paragraph p
left join projects_groupparagraph gp on p.id = gp.paragraph_id
where gp.group_id is null

