'''
    Any file within the no_import_common_class folder is for methods that can be
    imported safely (without circular dependencies) into the classes in
    the common class folder.
'''

import json
import os
from copy import deepcopy
from operator import itemgetter
import constants.para_lookup as lookup
import constants.scripts as constants


BEG_LINK_TEXT = '|beg|'
END_LINK_TEXT = '|end|'
RESUME = 'resume'
NOT_RESUME = ('exercise', 'flashcard')


def create_link(url, link_text):
    '''
    create_link: takes the input and creates a link to be used in displaying text

    :param url: will be a url to link to
    :type url: String
    :param link_text: will be the link text in the link taht will be created
    :type link_text: String
    :return: Link that will be used as a reference to its associated paragraph
    :rtype: String
    '''
    return f'<a href="{url}" class="reference_link" target="_blank">{link_text}</a>'


def json_to_dict(json_path):
    '''
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
    format_json_text takes a List of strings and concatenates them
       together with a space

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
    extract_data_from_form formats the Study lookup form return to be usable for
    queries

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


def add_paragraphs_by_group_to_context(context, paragraphs):
    '''
    add_paragraphs_by_group_to_context reformats data to save work in the template

    :param context: original context, minus what was needed for para retrieval
    :type context: dict
    :param paragraphs: paragraphs by group list before adding to context
    :type paragraphs: dict
    :return: context - will be used in various category templates
    :rtype: dict
    '''
    context['title'] = paragraphs['title']
    if 'side_menu' in paragraphs.keys():
        context['side_menu'] = paragraphs['side_menu']
    elif 'hidden_flashcard_divs' in paragraphs.keys():
        context['hidden_flashcard_divs'] = paragraphs['hidden_flashcard_divs']
    context['groups'] = paragraphs['groups']
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
    mid_link = '" class="para_by_subtitle modal_popup_link">'
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
    print(f'info=={info}')
    para['image_classes'] = info['classes']
    return para


def loop_through_files_for_db_updates(method, process_data):
    ''' Loops through files in directory and processes each individually '''
    directory = process_data['input_directory']
    num_processed = 0
    file_list = sorted_files_in_dir(directory, True)
    for filename in file_list:
        if use_file(filename, str(method), process_data):
            file_path = os.path.join(directory, filename)
            num_processed += 1
            process_data['file_data'] = json_to_dict(file_path)
            method(process_data)
        else:
            continue
    return num_processed


def sorted_files_in_dir(directory, descending=False):
    '''
    sorted_files_in_dir uses directory name to get list of files and sort it by filename

    :param directory: directory name and path
    :type directory: str
    :param descending: whether to sort alphebetically or in reverse, defaults to False
    :type descending: bool, optional
    :return: sorted list of files
    :rtype: list
    '''
    list_of_files = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            list_of_files.append(filename)
    list_of_files.sort(reverse=descending)
    return list_of_files


def use_file(filename, method, process_data):
    '''
    use_file returns false if the extension is not json

    If it is Step One, that is enough for use_file to return True

    If Step Three, need to check if production or running as if it's production:

    if production, use_file returns True if file has production prefix or
    if not production, use_file returns True if file does not have production prefix

    Otherwise use_file returns False

    :param filename: filename (without path)
    :type filename: str
    :param method: string representation of method name (tell whether step 1 or 3)
    :type method: str
    :param process_data: passed in: environment (from environment variable) or run_as_prod, script arg
    :type process_data: dictionary
    :return: Depending on factors mentioned above, pass back True if file is correct oe False, elsewise
    :rtype: bool
    '''
    if not filename.endswith(constants.JSON_SUB):
        return False
    if 'step_three' not in method:
        return True
    if treat_like_production(process_data):
        return filename.startswith(constants.PROD_PROCESS_IND)
    return not filename.startswith(constants.PROD_PROCESS_IND)


def treat_like_production(process_data):
    '''
    treat_like_production returns true if it is the production environment (is_prod is True) or
    if we are running as prod

    :param process_data: dictionary that contains is_prod and run_as_prod information
    :type process_data: dict
    :return: whether or not we should treat it like production
    :rtype: bool
    '''
    return process_data['is_prod'] or process_data['run_as_prod']

def flashcard_paragraph_layout(paras, collapse_id, cat_type='flashcard'):
    '''
    flashcard_paragraph_layout this will display the first paragraph and then do collapse for the other
    paragraphs

    :param paragraphs: array of paragraphs
    :type paragraphs: list
    '''
    first_para = paras.pop(0)
    html_output = format_one_para(first_para, cat_type)
    html_output += flashcard_wrap_answer(paras, collapse_id)
    return html_output


def flashcard_wrap_answer(paragraphs, collapse_id, cat_type='flashcard'):
    '''
    flashcard_wrap_answer wraps the answers in an accordian wrapper

    :param paragraphs: all the paragraphs minus the first one
    :type paragraphs: list of dicts
    :param collapse_id: the id of the collapsable div
    :type collapse_id: str
    :param cat_type: type of cateogory, this should always be flashcard, defaults to 'flashcard'
    :type cat_type: str, optional
    '''
    return('<div id="accordion">'
           '<div class="card">'
           '<div class="card-header collapsed card-link" data-toggle="collapse"'
           f'data-target="#{collapse_id}"">'
           '<div>Show Answer</div></div>'
           f'<div id={collapse_id} class="collapse" data-parent="#accordion">'
           f'<div class="card-body"><div>{paragraphs_for_category_pages(paragraphs, cat_type)}</div>'
           '</div></div>')


def paragraphs_for_category_pages(paragraphs, cat_type):
    '''
    paragraphs_for_category_pages concatenates paragraphs into a string

    :param paragraphs: all the paragraphs as processed for display
    :type paragraphs: dict
    :return: all the paragraph html concatenated into big string
    :rtype: str
    '''
    html_output = ''
    for para in paragraphs:
        html_output += format_one_para(para, cat_type)
    return html_output

def format_one_para(para, cat_type):
    html_output = ''
    if para['subtitle']:
        html_output += f'<h5><strong>{para["subtitle"]}</strong></h5>'
    if para['subtitle_note'] and cat_type in NOT_RESUME:
        html_output += f'<p>{para["subtitle_note"]}</p>'
    if para['image_path']:
        html_output += '<img class="' + para['image_classes'] + '" '
        html_output += 'src="' + f'static {para["image_path"]}" '
        html_output += f'alt="{para.image_alt}">'
    html_output += para['text']
    if para['subtitle_note'] and cat_type == RESUME:
        html_output += f'<p>{para["subtitle_note"]}</p>'
    return html_output
