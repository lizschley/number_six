'''These tests are for utilities to call paragraph helpers that instansiate the
   common classes. I am using '''
# pylint: disable=missing-function-docstring
import testing.constants.common as common


def test_display_para_from_json_returns_dictionary(display_text_from_json):
    '''This is an integration test, testing the json to paragraph display demo'''
    assert isinstance(display_text_from_json, dict)


def test_display_para_from_json_contains_correct_keys(display_text_from_json):
    '''This is an integration test, testing the json to paragraph display demo'''
    keys = list(display_text_from_json)
    keys.sort()
    assert keys == common.DISPLAY_PARA_KEYS


def test_paragraph_count_from_display_para(display_text_from_json):
    '''This is an integration test, testing the json to paragraph display demo'''
    para_list = display_text_from_json['paragraphs']
    assert len(para_list) == 2


def test_paragraph_has_references(display_text_from_json):
    '''This is an integration test, testing the json to paragraph display demo'''
    para_list = display_text_from_json['paragraphs']
    assert isinstance(para_list[0], dict)


def test_references_have_links(display_text_from_json):
    '''This is an integration test, testing the json to paragraph display demo'''
    ref = display_text_from_json['paragraphs'][0]['references']
    assert isinstance(ref, str)
    assert ref.find('href=') == 3
