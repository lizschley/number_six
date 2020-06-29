'''Tests for methods in helpers/no_import_common_class/paragraph_helpers.py'''
# pylint: disable=missing-function-docstring
import helpers.no_import_common_class.paragraph_helpers as para_helper
import testing.helpers.testing_helpers as testing_helper


def test_create_link():
    url: str = 'http://www.math.com/'
    link_text: str = 'Math'
    link: str = para_helper.create_link(url, link_text)
    assert link == '<a href="http://www.math.com/" target="_blank">Math</a>'


def test_json_to_dict(basic_paragraph_dict_file, request):
    return_dict = testing_helper.get_basic_para_cache(basic_paragraph_dict_file, request)
    assert isinstance(return_dict, dict)


def test_format_of_paragraph_dictionary(basic_paragraph_dict_file, request):
    return_dict = testing_helper.get_basic_para_cache(basic_paragraph_dict_file, request)
    assert isinstance(return_dict, dict)
