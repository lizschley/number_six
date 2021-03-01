select string_agg(distinct cast (p.id as varchar), ',') as para_ids
from projects_paragraph p
join projects_groupparagraph gp on gp.paragraph_id = p.id
where gp.group_id = 14
