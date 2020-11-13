'''
    Any file within the no_import_common_class folder is for methods that can be
    imported safely (without circular dependencies) into the classes in
    the common class folder.

    These methods are specific to category pages
'''

RESUME = 'resume'
NOT_RESUME = ('exercise', 'flashcard')


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


def flashcard_paragraph_layout(paras, collapse_id, ref_links, cat_type='flashcard'):
    '''
    flashcard_paragraph_layout this will display the first paragraph and then do collapse for the other
    paragraphs

    :param paragraphs: array of paragraphs
    :type paragraphs: list
    '''
    first_para = paras.pop(0)
    html_output = format_one_para(first_para, cat_type)
    html_output += flashcard_wrap_answer(paras, collapse_id, ref_links)
    return html_output


def flashcard_wrap_answer(paragraphs, collapse_id, ref_links, cat_type='flashcard'):
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
           '<div>Toggle Answer</div></div>'
           f'<div id={collapse_id} class="collapse" data-parent="#accordion">'
           '<div class="card-body"><div>'
           f'{paragraphs_for_category_pages(paragraphs, cat_type, ref_links)}</div>'
           '</div></div>')


def paragraphs_for_category_pages(paragraphs, cat_type, ref_links=''):
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
    if cat_type == 'flashcard':
        html_output += '<h5>References</h5>'
        html_output += ref_links
    return html_output


def format_one_para(para, cat_type):
    '''
    format_one_para adds html coding here, because it is simpler than adding it in
    templates

    :param para: a paragraph field after it gets formatted like in basic display_paragraphs
    :type para: dict
    :param cat_type: type of category, for example flashcard, resume or exercise
    :type cat_type: string
    :return: html that will be added to the group to be output by the appropriate category displayer
    :rtype: str
    '''
    html_output = ''
    if para['subtitle']:
        html_output += f'<h5><strong>{para["subtitle"]}</strong></h5>'
    if para['subtitle_note'] and cat_type in NOT_RESUME:
        html_output += f'<p>{para["subtitle_note"]}</p>'
    if para['image_path']:
        html_output += '<div class="text-center">'
        html_output += '<img class="' + para['image_classes'] + '" '
        html_output += 'src="/static/' + para['image_path'] + '" '
        html_output += 'alt="' + para['image_alt'] + '">'
        html_output += '</div>'
    html_output += para['text']
    if para['subtitle_note'] and cat_type == RESUME:
        html_output += f'<p>{para["subtitle_note"]}</p>'
    return html_output
