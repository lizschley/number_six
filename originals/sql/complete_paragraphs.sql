select c.id as category_id, c.title, c.category_type, g.id as group_id, g.title as group_title, g.note as title_note,  
                p.id as paragraph_id, subtitle, text, p.note as subtitle_note, 
                r.id as reference_id, link_text, url
            from
               projects_group g
            join projects_groupparagraph gp on g.id = gp.group_id
            join projects_paragraph p on p.id = gp.paragraph_id
            join projects_paragraphreference pr on p.id = pr.paragraph_id
            join projects_reference r on r.id = pr.reference_id
            left outer join projects_category c on c.id = g.category_id
order by c.title, g.title, p.subtitle, r.link_text
