''' Constants used for resume screen scraping '''

COMPANY_SUBSTR = ('Medical', 'LexisNexis', 'Teachstone', 'Construct')
LOOKING_FOR = {
    'work_experience': 'Work Experience',
    'education': 'Education',
}

TECH_LIST = ('Python, Ruby, Rails, Java, JavaScript, jQuery, HTML5, SCSS, Selenium, Pytest'
             'Rspec, VBA with MS Project, C# (Visual Studio), MySql, Postgres, SQL Server, IDMS,'
             'Sybase, IDMS, SAS, JSP, STRUTS, XML, XSLT, Web Services, SQL, ASP')

TEXT = {
    'beg_para': '<ul><li>',
    'end_para': '</li></ul>',
    'beg_tech_list': '<br><strong>Technologies:</strong> ',
    'beg_company': '<br><strong>Company:</strong> ',
}

COMPANIES = {
    'Medical': 'Medical Automation Systems (Abbott), Project Manager, 2007 - 2012',
    'LexisNexis': 'LexisNexis, Senior Software Engineer, 1993 - 2007',
    'Teachstone': "Teachstone Training, Backend Web Developer, 2013 - 2019",
    'Construct': 'CoConstruct, QA Automation Engineer, 2019 - 2020 (5 months)',
}
