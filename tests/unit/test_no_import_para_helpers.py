'''Tests for methods in helpers/no_import_common_class/paragraph_helpers.py'''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
import pytest
import helpers.no_import_common_class.lookup_form_helpers as form_helper
import helpers.no_import_common_class.paragraph_helpers as para_helper
import testing.data.list_constants as list_data
import testing.helpers.testing_helpers as helper
from common_classes.paragraphs_for_display import ParagraphsForDisplay


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


@pytest.mark.parametrize('substring', [('http://www.math.com/'),
                                       ('Math'),
                                       ('reference_link')])
def test_create_link(substring):
    url: str = 'http://www.math.com/'
    link_text: str = 'Math'
    link: str = para_helper.create_link(url, link_text)
    assert substring in link


def test_json_to_dict(orig_para_dict_data):
    assert isinstance(orig_para_dict_data, dict)


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
    ajax_args = ParagraphsForDisplay.AJAX_ARGS
    ajax_args['from_ajax'] = from_ajax
    return_para = para_helper.replace_link_indicators(para_helper.ajax_link,
                                                      para_with_indicators, **ajax_args)

    assert return_para_correct(return_para, from_ajax)


@pytest.mark.parametrize('substring', [('data-subtitle="testing text is actual subtitle not link_text"'),
                                       ('>test link text</a>'),
                                       ('data-subtitle="sub_2"'),
                                       ('>sub_2</a>')])
def test_substitute_real_subtitle_ajax_link(substring):
    start_para = 'preceding |beg|test link text|end| inbetween text |beg|sub_2|end| following text'
    ajax_args = ParagraphsForDisplay.AJAX_ARGS
    ajax_args['from_ajax'] = False
    fullstring = para_helper.replace_link_indicators(para_helper.ajax_link, start_para, **ajax_args)
    helper.assert_in_string(fullstring, substring)


def check_text_para_assertions(text, check_for='<p>', pos=0):
    assert isinstance(text, str)
    assert text.find(check_for) == pos


def return_para_correct(ret_text, from_ajax):
    print(f'return text == {ret_text}')
    if from_ajax:
        print(f'if from ajax return text == {ret_text}')
        expected_text = 'preceding sub_1 inbetween text sub_2 sub_3 following text'
    else:
        print(f'else return text == {ret_text}')
        expected_text = (
            'preceding '
            '<a href="#" data-subtitle="sub_1" class="para_by_subtitle modal_popup_link">sub_1</a> '
            'inbetween text '
            '<a href="#" data-subtitle="sub_2" class="para_by_subtitle modal_popup_link">sub_2</a> '
            '<a href="#" data-subtitle="sub_3" class="para_by_subtitle modal_popup_link">sub_3</a> '
            'following text')
    return ret_text == expected_text
