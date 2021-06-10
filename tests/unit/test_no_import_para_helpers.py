'''Tests for methods in helpers/no_import_common_class/paragraph_helpers.py'''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
import pytest
import helpers.no_import_common_class.paragraph_helpers as para_helper
import helpers.no_import_common_class.lookup_form_helpers as lookup_helper
import testing.data.list_constants as list_data


@pytest.fixture()
def add_para_to_context_input():
    return {
        'context': {'whatever': 'it is'},
        'paragraphs': {'title': 'title',
                       'title_note': 'note',
                       'group_type': 'standalone',
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
    input_from_form = {'ordered': '0', 'standalone': 'group_21', 'flashcard': '0', 'search': ''}
    output = lookup_helper.process_form_data(input_from_form)
    assert isinstance(output, dict)
    assert output == {'group': 21}


def test_add_paragraphs_to_context(add_para_to_context_input):
    res = para_helper.add_paragraphs_to_context(add_para_to_context_input['context'],
                                                add_para_to_context_input['paragraphs'])
    return_keys = set(res.keys())
    set_data = set(list_data.KEYS_FOR_PARA_DISPLAY_CONTEXT)
    assert set_data == set_data & return_keys


def test_format_group_id(group_id):
    assert lookup_helper.format_group_id(group_id) == 'group_23'
