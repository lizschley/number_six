update projects_paragraph set note = note || '<br><br>'
where note like('Text was%')
