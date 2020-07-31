'''Tests for methods in helpers/no_import_common_class/paragraph_helpers.py'''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
import pytest
import helpers.no_import_common_class.lookup_form_helpers as form_helper
import helpers.no_import_common_class.paragraph_helpers as para_helper
import testing.data.list_constants as list_data
import testing.helpers.testing_helpers as helper


@pytest.fixture()
def add_para_to_context_input():
    return {
        'context': {'whatever': 'it is'},
        'paragraphs': {'title': 'title',
                       'title_note': 'note',
                       'paragraphs': ['para1', 'para2', 'para3']}
    }


@pytest.fixture()
def group_id():
    return 23


@pytest.fixture()
def para_with_indicators():
    return 'preceding |beg|sub_1|end| inbetween text |beg|sub_2|end| |beg|sub_3|end| following text'


def test_create_link():
    url: str = 'http://www.math.com/'
    link_text: str = 'Math'
    link: str = para_helper.create_link(url, link_text)
    assert link == '<a href="http://www.math.com/" target="_blank">Math</a>'


def test_json_to_dict(orig_para_dict_data):
    assert isinstance(orig_para_dict_data, dict)


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


def test_add_paragraphs_to_context(add_para_to_context_input):
    res = para_helper.add_paragraphs_to_context(add_para_to_context_input['context'],
                                                add_para_to_context_input['paragraphs'])
    return_keys = set(res.keys())
    set_data = set(list_data.KEYS_FOR_PARA_DISPLAY_CONTEXT)
    assert set_data == set_data & return_keys


def test_format_group_id(group_id):
    assert form_helper.format_group_id(group_id) == 'group_23'


@pytest.mark.parametrize('from_ajax', [(True), (False)])
def test_replace_ajax_link_indicators(para_with_indicators, from_ajax):
    return_para = para_helper.replace_ajax_link_indicators(para_with_indicators, from_ajax)
    assert return_para_correct(return_para, from_ajax)


@pytest.mark.parametrize('substring', [('data-subtitle="longer text that is the actual subtitle"'),
                                       ('>short link text</a>'),
                                       ('data-subtitle="sub_2"'),
                                       ('>sub_2</a>')])
def test_substitute_real_subtitle_ajax_link(substring):
    start_para = 'preceding |beg|short link text|end| inbetween text |beg|sub_2|end| following text'
    fullstring = para_helper.replace_ajax_link_indicators(start_para, False)
    helper.assert_in_string(fullstring, substring)


def check_text_para_assertions(text, check_for='<p>', pos=0):
    assert isinstance(text, str)
    assert text.find(check_for) == pos


def return_para_correct(ret_text, from_ajax):
    if from_ajax:
        expected_text = 'preceding sub_1 inbetween text sub_2 sub_3 following text'
    else:
        expected_text = ('preceding '
                         '<a href="#" data-subtitle="sub_1" class="para_by_subtitle">sub_1</a> '
                         'inbetween text '
                         '<a href="#" data-subtitle="sub_2" class="para_by_subtitle">sub_2</a> '
                         '<a href="#" data-subtitle="sub_3" class="para_by_subtitle">sub_3</a> '
                         'following text')
    return ret_text == expected_text
