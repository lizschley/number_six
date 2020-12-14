''' These methods help display the form used in the study form '''
from projects.models.paragraphs import Group, Category

STUDY_CATEGORIES = ['flashcard', 'study']
INIT_STANDALONE = ('0', 'Choose Standalone Paras (i.e. Definitions or About)')
INIT_ORDERED = ('0', 'Choose Ordered Paras (i.e. Instructions)')
INIT_FLASHCARDS = ('0', 'Choose Flashcards (i.e. Questions and Answers)')


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
