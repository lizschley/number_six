'''These are methods designed for use outside of the common classes.  The file
   imports the common classes, creating a risk of circluar dependencies.'''
import os
import helpers.no_import_common_class.paragraph_helpers as para_helper
import portfolio.settings as settings
from common_classes.paragraph_retriever import ParagraphRetriever
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


# to run in >> python manage.py shell
# import helpers.import_common_class.paragraph_helpers as para_helper
# paragraphs = para_helper.retrieve_paragraphs_manual_testing()
def retrieve_paragraphs_manual_testing():
    '''Maybe should delete this and replace it with automated testing.
       It was used for manual testing '''
    paragraphs = ParagraphRetriever()
    res = paragraphs.retrieve_input_data(group_id=None, search_str=None,
                                         path_to_json=DEMO_PARAGRAPH_JSON)
    print(res)
    return paragraphs


def paragraph_view_input(context):
    '''
    paragraph_view_input extracts arguments for paragraph retrieval from context
    and then uses them to retrieve paragraphs, references, etc

    :param context: para views, for ex: demo_paragraphs & study_paragraphs_with_group
    :type context: dict
    :return: context with the paragraphs added
    :rtype: dict
    '''
    # print(f'in paragraph_helpers.context_to_paragraphs, context=={context}')
    path_to_json = context.pop('path_to_json', None)
    group_id = context.pop('group_id', None)
    search_str = context.pop('search_str', None)
    # print(f'after popping, context=={context}')

    # retrieve data
    paragraphs = ParagraphsForDisplay()
    paragraphs = paragraphs.retrieve_paragraphs(path_to_json=path_to_json, group_id=group_id,
                                                search_str=search_str)

    # print output
    # print(f'after calling retrieve paragraphs returned data == {paragraphs}')
    context = add_paragraphs_to_context(context, paragraphs)
    # print(f'after adding paragraphs to context, context=={context}')
    return context


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
