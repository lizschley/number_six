''' This is for list data that is stored in constants and used for Testing'''


PARA_DISPLAY_OUTPUT_DATA_FOR_TESTING = {
    'paragraphs': [
        {
            'id': 'first',
            'references': '<a href="https://literature.org/" target="_blank">literature</a><br>',
            'subtitle': 'Fiction',
            'subtitle_note': '* Note - only public domain for listening to fall asleep.',
            'text': '<p>Fiction is my number one non-domestic animal  love.  My '
            'favorite animal is Rick.  He shares my love of fiction.</p>'
        },
        {
            'id': 'second',
            'references': '<a href="https://gymcastic.com/" '
            'target="_blank">JessicaSpencerKensley</a><br>',
            'subtitle': 'A sometimes wonderful, but often annoying podcast',
            'subtitle_note': '',
            'text': '<p>Jessica, Spencer and Kensley are fun to listen to. Jessica '
                    'and Spencer can be annoying, but Kensley rarely is. But like '
                    'the way I feel about my cats,  I  like them all equally in spite '
                    'of their natures.</p>'
        }],
    'title': 'Listening',
    'title_note': '*Note - subjects I listen to'
}

PARA_DISPLAY_INPUT_DATA_FOR_TESTING = {
    'group': {
        'title': 'Listening',
        'note': '*Note - subjects I listen to'
    },
    'references': [{
        'link_text': 'Literature',
        'url': 'https://literature.org/'
    }, {
        'link_text': 'JessicaSpencerKensley',
        'url': 'https://gymcastic.com/'
    }],
    'paragraphs': [{
        'id': 'first',
        'subtitle': 'Fiction',
        'note': '* Note - only public domain for listening to fall asleep.',
        'text': '<p>Fiction is my number one non-domestic animal  love.  My favorite animal is Rick.  He shares my love of fiction.</p>',
        'order': 'fiction'
    }, {
        'id': 'second',
        'subtitle': 'A sometimes wonderful, but often annoying podcast',
        'note': '',
        'text': '<p>Jessica, Spencer and Kensley are fun to listen to. Jessica and Spencer can be annoying, but Kensley rarely is. But like the way I feel about my cats,  I  like them all equally in spite of their natures.</p>',
        'order': 'a sometimes wonderful, but often annoying podcast'
    }],
    'para_id_to_link_text': {
        'first': ['Literature'],
        'second': ['JessicaSpencerKensley']
    }
}