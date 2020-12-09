'''Unit tests for ParagraphsForDisplay.  Note - sometimes test multiple methods at a time'''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

import pytest
from common_classes.paragraphs_for_display_one import ParagraphsForDisplayOne
from common_classes.paragraphs_for_display import ParagraphsForDisplay
import testing.data.dict_constants as constants
import testing.helpers.testing_helpers as helper


@pytest.fixture()
def paragraphs_for_display_one_object():
    paragraph = ParagraphsForDisplayOne()
    paragraph.input_data = constants.PARA_DISPLAY_ONE_PARA_INPUT
    return paragraph


@pytest.mark.parametrize('var_name, var_type', [('group_title', str),
                                                ('group_note', str),
                                                ('reference_links', dict),
                                                ('paragraphs', list),
                                                ('input_data', dict)])
def test_paragraphs_for_display_one_init(paragraphs_for_display_one_object, var_name, var_type):
    helper.assert_instance_variable(paragraphs_for_display_one_object, var_name, var_type)


def test_create_links_from_references(paragraphs_for_display_one_object):
    paragraphs_for_display_one_object.create_links_from_references()
    ref_links = paragraphs_for_display_one_object.reference_links
    assert len(paragraphs_for_display_one_object.reference_links) == 1
    assert 'https://www.yourdictionary.com/glabrous' in ref_links['YourDictionary_glabrous']


def test_assign_paragraphs(paragraphs_for_display_one_object):
    '''this also tests add_links_to_paragraphs and paragraph_links'''
    paragraphs_for_display_one_object.create_links_from_references()
    paragraphs_for_display_one_object.assign_paragraphs()
    paras = paragraphs_for_display_one_object.paragraphs
    assert len(paras) == 1
    assert isinstance(paras[0]['references'], str)
    assert 'href=' in paras[0]['references']
    assert paras[0]['id'] == 68
    assert paras[0]['subtitle'] == 'glabrous'


def test_paragraph(paragraphs_for_display_one_object):
    para = paragraphs_for_display_one_object.input_data['paragraphs'][0]
    return_para = ParagraphsForDisplay.paragraph(para)
    assert isinstance(return_para, dict)
    assert return_para['id'] == para['id']
    assert return_para['subtitle'] == para['subtitle']
    assert return_para['text'] == para['text']
    assert return_para['references'] == ''


@pytest.mark.parametrize('key', [('title'),
                                 ('title_note')])
def test_output_for_display_not_keys(paragraphs_for_display_one_object, key):
    paragraphs_for_display_one_object.title = paragraphs_for_display_one_object.input_data['group']['title']
    paragraphs_for_display_one_object.title_note = paragraphs_for_display_one_object.input_data['group']['note']
    out = paragraphs_for_display_one_object.output_single_para_display('glabrous')
    assert isinstance(out, dict)
    helper.assert_key_not_in_dictionary(out, key)


@pytest.mark.parametrize('key', [('references'),
                                 ('subtitle'),
                                 ('subtitle_note'),
                                 ('text')])
def test_output_for_display_keys(paragraphs_for_display_one_object, key):
    paragraphs_for_display_one_object.title = paragraphs_for_display_one_object.input_data['group']['title']
    paragraphs_for_display_one_object.title_note = paragraphs_for_display_one_object.input_data['group']['note']
    out = paragraphs_for_display_one_object.output_single_para_display('glabrous')
    assert isinstance(out, dict)
    helper.assert_key_in_dictionary(out, key)


@pytest.mark.parametrize('key, substring', [('references', 'YourDictionary_glabrous'),
                                            ('subtitle', 'Glabrous'),
                                            ('text', 'no hairs or pubescence')])
def test_output_for_display_values(paragraphs_for_display_one_object, key, substring):
    out = paragraphs_for_display_one_object.format_single_para_display('glabrous')
    assert isinstance(out, dict)
    helper.assert_in_string(out[key], substring)
