''' Methods to use for batch updates or whatever is needed'''
from django.utils.text import slugify
from projects.models.paragraphs import Group, Paragraph, Reference
from common_classes.para_db_methods import ParaDbMethods
from common_classes.para_link_helper import ParaLinkHelper
import constants.para_lookup as lookup
from utilities.record_dictionary_utility import RecordDictionaryUtility


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


def update_slugs_field_and_links(class_, updating=False, **kwargs):
    '''
    update_slugs_field_and_links finds the class using the old_slug and then updates the slug with
    the new slug

    kwargs = {
        'title_fieldname': '',
        'title_value': '',
        'existing_slug': ''
    }

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


def one_time_get_content(out_dir):
    ''' fix references to be consistant '''
    list_output = []
    para_ids = []
    references = Reference.objects.all().values()
    out_directory = {'directory_path': out_dir}
    for ref in references:
        link_text = ref['link_text']
        short_text = ref['short_text']
        ref_slug = ref['slug']
        if no_work_required(link_text, short_text):
            continue
        para_ids = add_to_para_id_list_if_necessary(ref_slug, para_ids)
        list_output.append(ref)
    print(f'paras to update== {",".join(para_ids)}')
    RecordDictionaryUtility.write_dictionary_to_file(list_output, **out_directory)


def no_work_required(link_text, short_text):
    ''' Return True if there is no plan to fix this reference else False '''
    chars = set('0123456789')
    if not any((c in chars) for c in link_text):
        return True
    temp = link_text.split('_')
    if len(temp) < 2:
        return True
    if not any((c in chars) for c in short_text):
        return False
    if temp[0][0] in '123456789':
        return True
    if temp[1][0] in '123456789':
        return True
    return False


def add_to_para_id_list_if_necessary(ref_slug, para_ids):
    ''' This is potentially useful elsewhere, maybe if I ever make a utility to update slugs once we
        have a production environment used with one_time_get_content(out_dir) from
        record_dictionary_utility
    '''
    try:
        para = Paragraph.objects.get(text__icontains=ref_slug)
    except Paragraph.DoesNotExist:
        return para_ids
    para_ids.append(str(para.id))
    return para_ids
