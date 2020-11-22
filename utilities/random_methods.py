''' Methods that are not specific to Paragraph functionality, but could be useful '''
from django.utils.text import slugify


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


def inline_link_helper(link_text, url, inline_link_text):
    '''
    inline_link_helper When creating new inline links &/or references, call this and add results to
    constants/para_lookup.  The INLINE_LINK_LOOKUP constant in the Para_lookup file
    is used to make inline links consitent and hopefully less work.

    :param link_text: This is the reference link text, is always unique and stored in the database
    :type link_text: str
    :param url: This is an outside html link
    :type url: str
    :param inline_link_text: This is more user friendly link text, for using in the text para
    :type inline_link_text: str
    :return: a lookup table entry to convert |beg_ref_slug|actual_ref_slug|beg_ref_slug| to inline link
    :rtype: dict
    '''
    key = slugify(link_text)
    return {key: {'url': url,
                  'link_text': inline_link_text}}
