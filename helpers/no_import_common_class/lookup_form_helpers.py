''' These methods help display the form used in the study form '''
from projects.models.paragraphs import Group, Category

STUDY_CATEGORIES = ['flashcard', 'study']
INIT_STANDALONE = ('0', 'Choose Standalone Paras (i.e. Definitions or About)')
INIT_ORDERED = ('0', 'Choose Ordered Paras (i.e. Instructions)')
INIT_FLASHCARDS = ('0', 'Choose Flashcards (i.e. Questions and Answers)')

EXPECTED_GET_VARIABLES = ['standalone', 'flashcard', 'ordered']

def study_dropdowns():
    group_lists = {}
    group_lists['flashcard'] = list_flaschards()
    group_lists['ordered'] = [INIT_ORDERED]
    group_lists['standalone'] = [INIT_STANDALONE]
    return organize_group_lists(group_lists)


def list_flaschards():
    flashcard_list = [INIT_FLASHCARDS]
    categories = Category.objects.filter(category_type__in=['flashcard'])
    for category in categories:
        cat_display = category.title
        flashcard_list.append((format_category_id(category.pk), cat_display))
    return flashcard_list


def organize_group_lists(dropdown_lists):
    groups = Group.objects.filter(category__category_type='study')
    for group in groups:
        if group.group_type == 'ordered':
            dropdown_lists['ordered'].append((format_group_id(group.pk), group.title))
        elif group.group_type == 'standalone':
            dropdown_lists['standalone'].append((format_group_id(group.pk), group.title))
    return dropdown_lists


def format_group_id(group_id):
    '''
    format_group_id makes it so the study dropdown id field can display ids for different tables

    :param group_id: int
    :type group_id: str
    :return: used as the id in the study dropdown
    :rtype: str
    '''
    return 'group_' + str(group_id)


def format_category_id(category_id):
    '''
    format_category_id makes it so the study dropdown id field can display ids for different tables

    :param category_id: int
    :type category_id: str
    :return: used as the id in the study dropdown
    :rtype: str
    '''
    return 'category_' + str(category_id)


def extract_data_from_form(input_from_form):
    '''
    extract_data_from_form takes the user choices from the lookup form to do data lookup

    :param input_from_form: input from the form
    :type input_from_form: dict
    :return: data in a form ready to use in where statements
    :rtype: dict
    '''
    in_data = {}
    for key in EXPECTED_GET_VARIABLES:
        if not input_from_form[key]:
            continue
        if input_from_form[key][0] == '0':
            continue
        in_data = create_dictionary_from_form_input(input_from_form[key][0])
    return in_data


def create_dictionary_from_form_input(data_from_form):
    '''
    create_dictionary_from_form_input formats the Study lookup form return to be usable for queries

    This takes data that is sent directly from the Study lookup form and
    transforms it in a way that can be used for view paramaters.  This is so the
    correct queries can be performed in the view.

    :param data_from_form: string that has the fieldname and the value separated
        by an underscore
    :type data_from_form: str
    :return: dictionary with key and value parsed from the input data
    :rtype: dictionary
    '''
    temp = data_from_form.split('_')
    if len(temp) != 2:
        return {}
    try:
        return {temp[0]: int(temp[1])}
    except ValueError:
        return {}
