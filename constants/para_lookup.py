''' used so that we can facilitate image patterns and save manual labor '''

IMAGE_INFO_LOOKUP = {
    'default': {'classes': 'img-fluid float-sm-left px-2'},
    'tall-skinny': {'classes': 'img-fluid px-2 float-sm-left tall-skinny'},
    'question': {'classes': 'img-fluid px-2'}
}

'''Used so that links do not need to exactly match subtitiles to be used in single para lookup'''
SUBTITLE_LOOKUP = {
    'test link text': 'testing text is actual subtitle not link_text',
    'Chinese Holly': 'Ilex-cornuta; Chinese Holly, Horned Holly',
}

INLINE_LINK_LOOKUP = {
    '20200528_mdn_subresourceintegrity': {
        'url': 'https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity',
        'link_text': 'MDN'
    },
    'nc_cooperativeextension_planttoolbox_erechtiteshie': {
        'url': 'https://plants.ces.ncsu.edu/plants/erechtites-hieraciifolius/',
        'link_text': 'NC Extension'
    },
    'friendswildflowergardenerechtiteshieraciifolius': {
        'url': 'https://www.friendsofthewildflowergarden.org/pages/plants/burnweed.html',
        'link_text': 'Friends of Wildflower'
    },
    '20201016_wikipedia_robertcmartin': {
        'url': 'https://en.wikipedia.org/wiki/Robert_C._Martin',
        'link_text': 'Robert C. Martin'
    },
    'twitter_mfeathers_michaelfeathers': {
        'url': 'https://twitter.com/mfeathers',
        'link_text': 'Michael Feathers'
    },
    'homebrewmissingpackagemanagermacoslinux': {
        'url': 'https://brew.sh/',
        'link_text': 'Homebrew Page'
    },
    'homebrewmissingpackagemanager_formulaprintscreen': {
        'url': 'https://brew.sh/',
        'link_text': 'printscreen from Homebrew page'
    },
    'jessicalaughlin_202002_howdoeshomebrewwork': {
        'url': 'https://medium.com/@jldlaughlin/how-does-homebrew-work-starring-rust-94ae5aa24552',
        'link_text': 'Jessica Laughlin Homebrew'
    },
    'homebrewdocumentation': {
        'url': 'https://docs.brew.sh/',
        'link_text': 'Homebrew Documentation'
    }
}
