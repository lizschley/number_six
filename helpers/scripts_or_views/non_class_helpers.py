from common_classes.paragraphs_for_display import ParagraphsForDisplay
from common_classes.paragraph_retriever import ParagraphRetriever
from common_classes.paragraphs_to_db import ParagraphsToDatabase
import helpers.classes_or_scripts.paragraph_helpers as ph
import os
import portfolio.settings as ps

DEMO_PARAGRAPH_JSON = os.path.join(ps.JSON_DATA_ROOT, 'demo/urban_coyotes.json')


def paragraph_list_from_json(json_path):
    paragraphs = ParagraphsForDisplay()
    return paragraphs.retrieve_paragraphs(path_to_json=json_path)


def paragraph_json_to_db(json_path):
    dict_data = ph.json_to_dict(json_path)
    paragraphs = ParagraphsToDatabase()
    paragraphs.dictionary_to_db(dict_data)


# import helpers.scripts_only.db_update_helpers as dbh
# paragraphs = dbh.retrieve_paragraphs_manual_testing()
def retrieve_paragraphs_manual_testing():
    paragraphs = ParagraphRetriever(group_id=None, search_str=None, path_to_json=DEMO_PARAGRAPH_JSON)
    res = paragraphs.return_formatted_input_to_display()
    print(res)
    return paragraphs


def paragraph_view_input(context):
    # extract arguments for paragraph retrieval from context
    print(f'in paragraph_helpers.context_to_paragraphs, context=={context}')
    path_to_json = context.pop('path_to_json', None)
    group_id = context.pop('group_id', None)
    search_str = context.pop('search_str', None)
    print(f'after popping, context=={context}')

    # retrieve data
    paragraphs = ParagraphsForDisplay()
    paragraphs = paragraphs.retrieve_paragraphs(path_to_json=path_to_json, group_id=group_id, search_str=search_str)

    # print output
    print(f'after calling retrieve paragraphs returned data == {paragraphs}')

    context = add_paragraphs_to_context(context, paragraphs)

    print(f'after adding paragraphs to context, context=={context}')
    return context


def add_paragraphs_to_context(context, paragraphs):
    context['title'] = paragraphs['title']
    context['title_note'] = paragraphs['title_note']
    context['paragraphs'] = paragraphs['paragraphs']
    return context

