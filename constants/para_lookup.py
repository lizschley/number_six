''' used so that we can facilitate image patterns and save manual labor '''

IMAGE_INFO_LOOKUP = {
    'default': {'classes': 'img-fluid  float-sm-left px-2'},
    'tall-skinny': {'classes': 'img-fluid px-2 float-sm-left tall-skinny'},
    'question': {'classes': 'img-fluid px-2'}
}

'''Used so that links do not need to exactly match subtitiles to be used in single para lookup'''
SUBTITLE_LOOKUP = {
    'test link text': 'testing text is actual subtitle not link_text',
    'Chinese Holly': 'Ilex-cornuta; Chinese Holly, Horned Holly',
}
