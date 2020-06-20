from projects.models.paragraphs import Group


INITIAL_CLASSIFICATION = [('0', 'Choose Classification')]


def get_initial_classifications():
    classification_list = INITIAL_CLASSIFICATION
    groups = Group.objects.all().order_by('id')
    for group in groups:
        classification_list.append((format_group_id(group.pk), group.title))
    return classification_list


def format_group_id(group_id):
    return 'group_' + str(group_id)

