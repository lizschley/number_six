''' Methods to use for batch updates or whatever is needed'''
from django.utils.text import slugify
from projects.models.paragraphs import Group, Paragraph, Reference
from common_classes.para_db_methods import ParaDbMethods
from common_classes.para_link_helper import ParaLinkHelper
import constants.para_lookup as lookup


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


# Todo: should this be a script?
def update_slugs_field_and_links(class_, updating=False, **kwargs):
    '''
    update_slugs_field_and_links finds the class using the old_slug and then updates the slug with
    the new slug

    kwargs are as follows:
        title_fieldname = kwargs['title_fieldname']
        title_new_value = kwargs['title_value']
        existing_slug = kwargs['existing_slug']

    IMPORTANT: Slugs should NOT be updated after the slugs are used in production for the following
    reasons:
        1. Group and Reference slugs are used to find records for updating
        2. If people bookmark something with slugs changing the slug will break the bookmark link

    :param class_: class with one instance of a slug that equals old_slug
    :type class_: models.Model from django.db
    :param updating: [description], defaults to False - will you be updating the record slugs
    :type updating: bool, optional
     '''
    title_fieldname = kwargs['title_fieldname']
    title_new_value = kwargs['title_value']
    existing_slug = kwargs['existing_slug']
    slug_new_value = slugify(title_new_value)
    updater = ParaDbMethods(updating)
    record = updater.find_record(class_, {'slug': existing_slug})
    update_dict = {'id': record.id, title_fieldname: title_new_value, 'slug': slug_new_value}
    updater.update_record(class_, update_dict)
    replace_slugs_in_paragraph_links(which_indicators(record),
                                     existing_slug, slug_new_value, updating)


def which_indicators(record):
    '''
    which_indicators associates the indicator to the class that will be used in the where statement
    for data retrieval.

    :param record: record associated with the links
    :type record: models.Model from django.db
    :return: Beginning and ending link indicators for the given record
    :rtype: dict
    '''
    if isinstance(record, Paragraph):
        return [lookup.AJAX_ARGS, lookup.PARA_ARGS]
    if isinstance(record, Group):
        return [lookup.GROUP_ARGS]
    if isinstance(record, Reference):
        return [lookup.REF_ARGS]
    return {}


def replace_slugs_in_paragraph_links(indicators, existing_slug, new_slug, updating=False):
    '''
    replace_slugs_in_paragraph_links is a convenience method that finds the paragraphs to update when
    slugs are updated.  You would actually run the above method: update_slugs_field_and_links
    Read the update_slugs_field_and_links comments for some caveats

    :param indicators: link indicators to know the type of links and records for the slugs (constants)
    :type indicators: dict
    :param existing_slug: slug value you will be replacing
    :type existing_slug: str
    :param new_slug: new slug value
    :type new_slug: str
    :param updating: [description], defaults to False - will you be updating the paragraph links
    :type updating: bool, optional
    '''
    kwargs = {'create_modal_links': False, 'para_link_slugs': True,
              'slug_data': {'existing_slug': existing_slug, 'new_slug': new_slug}}
    helper = ParaLinkHelper(**kwargs)
    paragraphs_to_update = helper.paragraph_slug_replacement(indicators)
    updater = ParaDbMethods(updating)
    for para in paragraphs_to_update:
        find_dict = {'id': para.id}
        create_dict = {'id': para.id, 'text': para.text}
        updater.find_and_update_record(Paragraph, find_dict, create_dict)
