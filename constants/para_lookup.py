''' used so that we can facilitate image patterns and save manual labor '''

IMAGE_INFO_LOOKUP = {
    'default': {'classes': 'img-fluid float-sm-left px-2 default'},
    'tall-skinny': {'classes': 'img-fluid px-2 float-sm-left tall-skinny'},
    'to-right': {'classes': 'img-fluid px-2 float-sm-right default'},
    'question': {'classes': 'img-fluid px-2'}
}

REF_ARGS = {'beg_link': '|beg_ref|', 'end_link': '|end_ref|'}
AJAX_ARGS = {'beg_link': '|beg|', 'end_link': '|end|'}
PARA_ARGS = {'beg_link': '|beg_para|', 'end_link': '|end_para|'}
GROUP_ARGS = {'beg_link': '|beg_group|', 'end_link': '|end_group|'}

INDICATOR_ARGS = (REF_ARGS, AJAX_ARGS, PARA_ARGS, GROUP_ARGS)
PARA_BEGIN = ('|beg|', '|beg_para|')
