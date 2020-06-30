'''Tests for methods in helpers/no_import_common_class/paragraph_helpers.py'''
# pylint: disable=missing-function-docstring
import helpers.no_import_common_class.paragraph_helpers as para_helper
import testing.data.list_constants as list_data


def test_create_link():
    url: str = 'http://www.math.com/'
    link_text: str = 'Math'
    link: str = para_helper.create_link(url, link_text)
    assert link == '<a href="http://www.math.com/" target="_blank">Math</a>'


def test_json_to_dict(basic_para_dict_data):
    assert isinstance(basic_para_dict_data, dict)


def test_format_json_text_without_para_tags():
    data = para_helper.format_json_text(list_data.TEXT_LIST_WITHOUT_PARA_TAGS)
    check_text_para_assertions(data)


def test_format_json_text_with_para_tags():
    data = para_helper.format_json_text(list_data.TEXT_LIST_WITH_PARA_TAGS)
    check_text_para_assertions(data)


def test_extract_data_from_form():
    classification = 'group_2'
    output = para_helper.extract_data_from_form(classification)
    assert isinstance(output, dict)
    assert output == {'group': 2}


def check_text_para_assertions(text, check_for='<p>', pos=0):
    assert isinstance(text, str)
    assert text.find(check_for) == pos
