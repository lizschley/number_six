''' These methods help display the form used in the study form '''
from projects.models.paragraphs import Group, Category

STUDY_CATEGORIES = ['flashcard']
INITIAL_CLASSIFICATION = [('0', 'Choose Classification')]


def get_initial_classifications():
    '''
    get_initial_classifications help with displaying data in a simple, but flexible
    way in the study lookup form

    This gets all of the groups for the study dropdown.  Later that dropdown will
    include some categories, so this will get more complex.

    :return: group_idx or (later) category_idx - where idx == the db id
    :rtype: str
    '''
    classification_list = INITIAL_CLASSIFICATION
    groups = Group.objects.filter(group_type__contains='study').order_by('slug')
    for group in groups:
        classification_list.append((format_group_id(group.pk), group.title))

    categories = Category.objects.filter(category_type__in=STUDY_CATEGORIES)
    for category in categories:
        cat_display = 'flashcards: ' + category.title
        classification_list.append((format_category_id(category.pk), cat_display))
    return classification_list


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
