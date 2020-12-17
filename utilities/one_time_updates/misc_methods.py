''' Methods to use for batch updates or whatever is needed'''
from django.utils.text import slugify
from projects.models.paragraphs import Group
from common_classes.para_db_methods import ParaDbMethods
from projects.models.paragraphs import Paragraph


DATA_TO_ADD = {
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


def add_short_text(updating=False):
    ''' use constant to update reference short_text fields '''
    updater = ParaDbMethods(updating)
    for key in DATA_TO_ADD:
        ref_data = DATA_TO_ADD[key]
        existing = updater.find_record(Reference, {'slug': key})
        print(f'found ref: {existing}')
        updater.find_and_update_record(Reference,
                                       {'id': existing.id},
                                       {'id': existing.id,
                                        'short_text': ref_data['link_text']
                                        })


def add_category_alter_group_type(updating=False):
    ''' one off for updating groups '''
    updater = ParaDbMethods(updating)
    groups = Group.objects.filter(group_type__contains='study').order_by('id')
    for group in groups:
        group_type = 'ordered' if 'ordered' in group.group_type else 'standalone'
        updater.find_and_update_record(Group,
                                       {'id': group.id},
                                       {'id': group.id,
                                        'cat_sort': None,
                                        'category_id': 5,
                                        'group_type': group_type,
                                        })


def add_slug_for_paragraphs_with_subtitles(updating=False):
    '''
    add_slug_for_paragraphs_with_subtitles adds slugs so that we can use for displaying paragraphs
    that are standalone (which require slugs)

    :param updating: use to test ahead of running, defaults to False
    :type updating: bool, optional
    '''
    updater = ParaDbMethods(updating)
    groups = Group.objects.all()
    for group in groups:
        new_slug = slugify(group.title)
        updater.find_and_update_record(Group,
                                       {'id': group.id},
                                       {'id': group.id,
                                        'slug': new_slug,
                                        })
