select r.id, r.slug, r.link_text, pr.paragraph_id
from projects_reference r
left join projects_paragraphreference pr on r.id = pr.reference_id
where pr.paragraph_id is null
