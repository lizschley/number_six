''' Constants used for resume screen scraping '''

COMPANY_SUBSTR = ('Medical', 'LexisNexis', 'Teachstone', 'Construct')
LOOKING_FOR = {'work_experience': 'Work Experience',
               'education': 'Education',
               }
TEXT = {'BEG_FIRST_PARA': '<ul><li>',
        'END_PARA': '</li>',
        'BEG_TECH_LIST': '<br><strong>Technologies:</strong> ',
        'BEG_COMPANY': '<br><strong>Company:</strong> ',
        'END_COMPANY': '</ul>',
}

COMPANIES = {
    'Medical': 'Medical Automation Systems (Abbott), Project Manager',
    'LexisNexis': 'LexisNexis, Senior Software Engineer',
    'Teachstone': "Teachstone Training, Backend Web Developer",
    'Construct': 'CoConstruct, QA Automation Engineer'
}

}