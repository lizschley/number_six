''' Methods that are not specific to Paragraph functionality, but could be useful '''


def valid_non_blank_string(str_to_check):
    '''
    valid_blank_string returns True if str_to_check is a valid string with more than just whitespace

    :param str_to_check: string to check
    :type str_to_check: str
    :return: True if it is a valid string that contains more than whitespace, else False
    :rtype: bool
    '''
    if not str_to_check:
        return False
    try:
        res = str_to_check.isspace()
    except AttributeError:
        return False
    return not res
