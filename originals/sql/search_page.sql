select g.id as group_id, g.group_type, g.slug,   
                p.id as para_id, p.standalone, p.slug as para_slug
            from
               projects_group g
            join projects_groupparagraph gp on g.id = gp.group_id
            join projects_paragraph p on p.id = gp.paragraph_id
            join projects_category c on c.id = g.category_id
            where c.category_type not in ('archived', 'resume')
            and group_type <> 'no_search'
            and (g.title like '%blue%' or p.subtitle like '%blue%' or p.text like '%blue%')
order by g.group_type, p.subtitle
