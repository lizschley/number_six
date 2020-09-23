'''These are methods designed for use outside of the common classes.  The file
   imports the common classes, creating a risk of circluar dependencies.'''
import helpers.no_import_common_class.paragraph_helpers as para_helper
from common_classes.paragraphs_for_display_one import ParagraphsForDisplayOne
from common_classes.paragraphs_for_display import ParagraphsForDisplay
from common_classes.para_db_create_process import ParaDbCreateProcess
from common_classes.para_db_update_prep import ParaDbUpdatePrep
from common_classes.para_db_update_process import ParaDbUpdateProcess
from common_classes.para_db_update_process_prod import ParaDbUpdateProcessProd


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


def paragraph_json_to_db(json_path, updating=False):
    '''
    paragraph_json_to_db
    Run by batch job to read a json file and update the database.  There is
    currently no return, though will probably in the future return ok or not ok

    :param json_path: path to json file
    :type json_path: string
    '''
    dict_data = para_helper.json_to_dict(json_path)
    paragraphs = ParaDbCreateProcess(updating)
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


def retrieve_paragraphs_based_on_context(paras, context):
    '''
    retrieve_paragraphs_based_on_context if someone chose a group in the lookup form
    use the group_id and id itself as kwargs

    :param paras: From .../projects/study/lookup to view (context) to then parameters to retrieve paras
    :type paras: ParagraphForDisplay object
    :param context: started with form output and then transform and add data as needed
    :type context: dict
    :return: input needed to display paragraphs
    :rtype: dict
    '''
    group_id = context.pop('group_id', None)
    if group_id is not None:
        return paras.retrieve_paragraphs(group_id=group_id)


def add_collapse_variables(paragraphs):
    '''
    add_collapse_variables adds the variables needed to collapse and expand paragraphs
    used for standalone paragraph display

    :param paragraphs: dictionary paragraphs - list of paragraphs
    :type paragraphs: dict containing list of individual paragraphs
    :return: list of paragraphs that have collapse variables for display
    :rtype:  dict containing list of individual paragraphs complete with collapse variables
    '''
    for para in paragraphs['paragraphs']:
        para['href_collapse'] = '#collapse_' + str(para['id'])
        para['collapse_id'] = 'collapse_' + str(para['id'])
        para['collapse_selector_id'] = '#collapse_' + str(para['id'])
    return paragraphs


def single_para_by_subtitle(subtitle):
    '''
    single_para_by_subtitle gets a single para with references by subtitle

    :param subtitle: from ajax link_text or from lookup table { 'link_text': 'real subtitle' }
    :type subtitle: str
    :return: one paragraph object (includes reference(s))
    :rtype: dict
    '''
    para = ParagraphsForDisplayOne()
    return para.retrieve_paragraphs(subtitle=subtitle)


def update_paragraphs_step_one(input_data):
    '''
    update_paragraphs_step_one is called by a batch process created to update data.

    The overall process is designed to work in both development and production.  But the prep
    happens only in development because the production database is the same as development.
    Once the manual process works seamlessly, the move data to production process can be
    automated.  Since the content needs to be created, however, this step will always be
    manual.

    :param input_data: Manually retrieved & updated data or, for production, retrieved by updated_date.
    :type input_data: dict
    :return: JSON file that to be manually edited for updates
    :rtype: writes JSON file
    '''
    updating = input_data.pop('updating', False)
    para = ParaDbUpdatePrep(input_data, updating)
    para.collect_data_and_write_json()


def update_paragraphs_step_three(input_data):
    '''
    update_paragraphs_step_three is called by a batch process created to update data.  There are two
    possible processes it can call:

    1. ParaDbUpdateProcess or 2. ParaDbUpdateProcessProd

    It will call the first one for the development process and the second one always if it is the
    production environment, but also if you run in development with the run_as_prod script argument

    :param input_data: data produced by Step one of the script or, if it is only for adding new data and
    is not run_as_prod or production, sent in directly

    :type input_data: dict
    '''
    # print(f'inside update_para_step 3, data == {input_data}')
    updating = input_data.pop('updating', False)
    para = input_data['class'](input_data, updating)
    print(f'running input_data["class"]: {input_data["class"].__name__}')
    para.process_input_data_update_db()
