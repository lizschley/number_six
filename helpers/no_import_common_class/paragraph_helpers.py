'''
    Any file within the no_import_common_class is for methods that can be
    imported safely (without circular dependencies) into the classes in
    the common class folder. '''

import json
import os
from operator import itemgetter
import constants.para_lookup as lookup

BEG_LINK_TEXT = '|beg|'
END_LINK_TEXT = '|end|'


def create_link(url, link_text):
    '''
    [Summary]
    create_link: takes the input and creates a link to be used in displaying text

    :param url: will be a url to link to
    :type url: String
    :param link_text: will be the link text in the link taht will be created
    :type link_text: String
    :return: Link that will be used as a reference to its associated paragraph
    :rtype: String
    '''
    return f'<a href="{url}" target="_blank">{link_text}</a>'


def json_to_dict(json_path):
    '''
    [Summary]
    json_to_dict takes a json file path, reads the content and uses it to create a dictionary.

    :param json_path: Path to a file on the project directory structure
    :type json_path: String
    :return: dictionary based on the contents of the JSON file
    :rtype: dictionary
    '''
    # Opening JSON file
    file = open(json_path, 'r')
    # load and return JSON object as a dictionary
    data = json.load(file)
    file.close()
    return data


def format_json_text(text):
    '''
    [Summary]
     format_json_text takes a List of strings and concatenates them
       together with a space

    [extended_summary]
    If there is no html tag (just checks for < in the first character),
       it adds a paragraph tag

    :param text: List of strings
    :type text: List
    :return: html formated text
    :rtype: str
    '''
    text = ' '.join(text)
    if text[0] != '<':
        text = '<p>' + text + '</p>'
    return text


def extract_data_from_form(classification):
    '''
    [Summary]
    extract_data_from_form formats the Study lookup form return to be usable for
    queries

    [extended_summary]
    This takes data that is sent directly from the Study lookup form and
    transforms it in a way that can be used for view paramaters.  This is so the
    correct queries can be performed in the view.

    :param classification: string that has the fieldname and the value separated
        by an underscore
    :type classification: str
    :return: dictionary with key and value parsed from the input data
    :rtype: dictionary
    '''
    temp = classification.split('_')
    if len(temp) != 2:
        return {}
    try:
        return {temp[0]: int(temp[1])}
    except ValueError:
        return {}


def add_paragraphs_to_context(context, paragraphs):
    '''
    add_paragraphs_to_context reformats data to save work in the template

    :param context: original context, minus what was needed for para retrieval
    :type context: dict
    :param paragraphs: paragraph dictionary before adding to context
    :type paragraphs: dict
    :return: context - will be used in paragraph template
    :rtype: dict
    '''
    context['title'] = paragraphs['title']
    context['title_note'] = paragraphs['title_note']
    context['paragraphs'] = paragraphs['paragraphs']
    return context


def sort_paragraphs(list_to_be_sorted, key_to_sort):
    '''
    sort_paragraphs sorts paragraphs

    :param list_to_be_sorted: paragraph list from paragraph retriever (has order field)
    :type list_to_be_sorted: sorted list of hashes
    '''
    return sorted(list_to_be_sorted, key=itemgetter(key_to_sort))


def check_for_batch_args(args, subs):
    '''
    This is for batch processing

    args is a tuple

    :param list_to_be_sorted: finds if substr is in args
    :type list_to_be_sorted: str
    '''
    return [i for i in args if subs in i]


def subtitle_lookup(orig):
    '''
    This is used to have ajax links for single paragraphs with long subtitles without
    using the whole subtitle as link text

    :param orig: orig is the link text that is used for the ajax lookup link
    :type: str
    :return: returns the actual subtitle.  May be from lookup table or may be passed in
    :rtype: str
    '''
    return lookup.SUBTITLE_LOOKUP[orig] if orig in lookup.SUBTITLE_LOOKUP.keys() else orig


def replace_ajax_link_indicators(para_text, from_ajax):
    '''
    replace_ajax_link_indicators -> contains indicators to say where I want links to definitions
    or other related standalone paragraphs that are in the database.  The look up is always
    by subtitle, though if the subtitle is too long, the link_text may be shorter.
    In that case the code finds the subtitle using a lookup table.

    :param para_text: paragraph['text']
    :type para_text: str
    :param from_ajax: If the para_text is from a ajax modal, just strip the indicators.
    :type from_ajax: bool
    :return: new para_text with the ajax modal link or the link indicators stripped
    :rtype: dict
    '''
    para_text = loop_through_text(para_text, from_ajax)
    return para_text


def loop_through_text(para_text, from_ajax):
    '''
    loop_through_text by splitting it using the indators: |beg| and |end|

    :param para_text: paragraph['text']
    :type para_text: str
    :param from_ajax: if the call is from ajax, then just strip the indicators
    :type from_ajax: bool
    :return: para_text with the links or para_text with the indicators stripped
    :rtype: str
    '''
    pieces = para_text.split(BEG_LINK_TEXT)
    para_piece_list = []
    for piece in pieces:
        if END_LINK_TEXT not in piece:
            para_piece_list.append(piece)
        else:
            sub_pieces = piece.split(END_LINK_TEXT)
            para_piece_list.append(ajax_link(sub_pieces[0], from_ajax))
            if len(sub_pieces) > 1:
                para_piece_list.append(sub_pieces[1])
    return ''.join(para_piece_list)


def ajax_link(orig_subtitle, from_ajax):
    '''
    ajax_link This creates an ajax link: looks up single para by subtitle and displays result in modal

    :param orig_subtitle: This will be the link text, though it may not be the actual subtitle
    :type orig_subtitle: str
    :param from_ajax: True if displaying text that has link indicators - avoiding links with modals
    :type from_ajax: bool
    :return: paragraph with link indicators turned into modal link or has link indicators stripped out
    :rtype: dict
    '''
    if from_ajax:
        return orig_subtitle
    substitute = lookup.SUBTITLE_LOOKUP
    beg_link = '<a href="#" data-subtitle="'
    mid_link = '" class="para_by_subtitle">'
    link_text = orig_subtitle
    end_link = '</a>'
    subtitle = orig_subtitle if orig_subtitle not in substitute.keys() else substitute[orig_subtitle]
    return beg_link + subtitle + mid_link + link_text + end_link


def add_image_information(para):
    '''
    add_image_information returns the information to display an image correctly or an unchanged para

    1. Path is in format to be used by template (originally from db or json input)
    2. Alt is based on the filename
    3. Classes are based on the image_info_key (from db or json input) to image_info lookup dictionary.

    :param para: para that is originally retrieved from JSON or db
    :type para: dict
    :return: para that has image information added, if there is an image path
    :rtype: dict
    '''

    if len(para['image_path']) == 0:
        para['image_alt'] = ''
        para['image_classes'] = ''
        return para
    para['image_alt'] = os.path.splitext(para['image_path'])[0]
    info = lookup.IMAGE_INFO_LOOKUP[para['image_info_key']]
    para['image_classes'] = info['classes']
    return para


