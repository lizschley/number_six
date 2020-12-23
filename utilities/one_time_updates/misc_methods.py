''' Methods to use for batch updates or whatever is needed'''
from django.utils.text import slugify
from projects.models.paragraphs import Group, Paragraph
from common_classes.para_db_methods import ParaDbMethods


def add_short_text(updating=False):
    ''' use subtitle to populate para short_title fields '''
    updater = ParaDbMethods(updating)
    paragraphs = Paragraph.objects.filter(standalone=True)
    for para in paragraphs:
        if (len(para.short_title) == 0 and len(para.subtitle) < 51):
            if not updating:
                print(para)
            updater.find_and_update_record(Paragraph,
                                           {'id': para.id},
                                           {'id': para.id,
                                            'short_title': para.subtitle})


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
