'''These are methods designed for use outside of the common classes.  The file
   imports the common classes, creating a risk of circluar dependencies.'''
import os
import helpers.no_import_common_class.paragraph_helpers as para_helper
import portfolio.settings as settings
from common_classes.paragraphs_for_display import ParagraphsForDisplay
from common_classes.paragraphs_to_db import ParagraphsToDatabase


DEMO_PARAGRAPH_JSON = os.path.join(settings.BASE_DIR, '/data/basic_paragraph.json')


def paragraph_list_from_json(json_path):
    '''
    paragraph_list_from_json reads JSON file that is formatted like the files
    used to upload data to the database.  Transforms it into a dictionary that
    can be passed to a display paragraph template

    :param json_path: path to the json file
    :type json_path: str
    :return: a dictionary formatted to best facilite displaying paragraphs
    :rtype: dict
    '''
    paragraphs = ParagraphsForDisplay()
    return paragraphs.retrieve_paragraphs(path_to_json=json_path)


def paragraph_json_to_db(json_path):
    '''
    paragraph_json_to_db
    Run by batch job to read a json file and update the database.  There is
    currently no return, though will probably in the future return ok or not ok

    :param json_path: path to json file
    :type json_path: string
    '''
    dict_data = para_helper.json_to_dict(json_path)
    paragraphs = ParagraphsToDatabase()
    paragraphs.dictionary_to_db(dict_data)


def paragraph_view_input(context, from_demo=False):
    '''
    paragraph_view_input extracts arguments for paragraph retrieval from context
    and then uses them to retrieve paragraphs, references, etc

    :param context: para views, for ex: demo_paragraphs & study_paragraphs_with_group
    :type context: dict
    :return: context with the paragraphs added
    :rtype: dict
    '''
    # retrieve data
    paragraphs = ParagraphsForDisplay()

    # print(f'in paragraph_helpers.context_to_paragraphs, context=={context}')
    if from_demo:
        path_to_json = context.pop('path_to_json', None)
        paragraphs = paragraphs.retrieve_paragraphs(path_to_json=path_to_json)
    else:
        paragraphs = retrieve_paragraphs_based_on_context(paragraphs, context)
        paragraphs = add_collapse_variables(paragraphs)

    context = para_helper.add_paragraphs_to_context(context, paragraphs)
    return context


# Todo: fill comment out correctly
def retrieve_paragraphs_based_on_context(paras, context):
    '''
    retrieve_paragraphs_based_on_context [summary]

    [extended_summary]

    :param paras: [description]
    :type paras: [type]
    :param context: [description]
    :type context: [type]
    :return: [description]
    :rtype: [type]
    '''
    group_id = context.pop('group_id', None)
    if group_id is not None:
        return paras.retrieve_paragraphs(group_id=group_id)
    subtitle = context.pop('subtitle', None)
    if subtitle is not None:
        return paras.retrieve_paragraphs(subtitle=subtitle)


# Todo: fill comment out correctly
def add_collapse_variables(paragraphs):
    '''
    add_collapse_variables [summary]

    [extended_summary]

    :param paragraphs: [description]
    :type paragraphs: [type]
    :return: [description]
    :rtype: [type]
    '''
    for para in paragraphs['paragraphs']:
        para['href_collapse'] = '#collapse_' + str(para['id'])
        para['collapse_id'] = 'collapse_' + str(para['id'])
    return paragraphs
