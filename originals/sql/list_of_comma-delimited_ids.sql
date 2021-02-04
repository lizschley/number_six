select string_agg(distinct cast (p.id as varchar), ',') as para_ids
from projects_paragraph p
where text like '%pyenv%'
