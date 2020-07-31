'''Unit tests for ParagraphsForDisplay.  Note - sometimes test multiple methods at a time'''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

import pytest
from common_classes.one_para_display import OneParaDisplay
from common_classes.paragraphs_for_display import ParagraphsForDisplay
import testing.data.dict_constants as constants
import testing.helpers.testing_helpers as helper


@pytest.fixture()
def one_para_display_object():
    paragraph = OneParaDisplay()
    paragraph.input_data = constants.PARA_DISPLAY_ONE_PARA_INPUT
    return paragraph


@pytest.mark.parametrize('var_name, var_type', [('title', str),
                                                ('title_note', str),
                                                ('reference_links', dict),
                                                ('paragraphs', list),
                                                ('input_data', dict)])
def test_one_para_display_init(one_para_display_object, var_name, var_type):
    helper.assert_instance_variable(one_para_display_object, var_name, var_type)


def test_create_links_from_references(one_para_display_object):
    one_para_display_object.create_links_from_references()
    ref_links = one_para_display_object.reference_links
    assert len(one_para_display_object.reference_links) == 1
    assert 'https://www.yourdictionary.com/glabrous' in ref_links['YourDictionary_glabrous']


def test_assign_paragraphs(one_para_display_object):
    '''this also tests add_links_to_paragraphs and paragraph_links'''
    one_para_display_object.create_links_from_references()
    one_para_display_object.assign_paragraphs()
    paras = one_para_display_object.paragraphs
    assert len(paras) == 1
    assert isinstance(paras[0]['references'], str)
    assert 'href=' in paras[0]['references']
    assert paras[0]['id'] == 68
    assert paras[0]['subtitle'] == 'glabrous'


def test_paragraph(one_para_display_object):
    para = one_para_display_object.input_data['paragraphs'][0]
    return_para = ParagraphsForDisplay.paragraph(para)
    assert isinstance(return_para, dict)
    assert return_para['id'] == para['id']
    assert return_para['subtitle'] == para['subtitle']
    assert return_para['text'] == para['text']
    assert return_para['references'] == ''



@pytest.mark.parametrize('key', [('title'),
                                 ('title_note')])
def test_output_for_display_not_keys(one_para_display_object, key):
    one_para_display_object.title = one_para_display_object.input_data['group']['title']
    one_para_display_object.title_note = one_para_display_object.input_data['group']['note']
    out = one_para_display_object.output_single_para_display('glabrous')
    assert isinstance(out, dict)
    helper.assert_key_not_in_dictionary(out, key)

# {'references': 'N/A', 'subtitle': 'Data not yet loaded ...==glabrous', 'subtitle_note': '', 'text': '<p>Either error or s...d yet.</p>'}
@pytest.mark.parametrize('key', [('references'),
                                 ('subtitle'),
                                 ('subtitle_note'),
                                 ('text')])
def test_output_for_display_keys(one_para_display_object, key):
    one_para_display_object.title = one_para_display_object.input_data['group']['title']
    one_para_display_object.title_note = one_para_display_object.input_data['group']['note']
    out = one_para_display_object.output_single_para_display('glabrous')
    print(f'out == {out}')
    assert isinstance(out, dict)
    helper.assert_key_in_dictionary(out, key)

@pytest.mark.parametrize('key, substring', [('references', 'YourDictionary_glabrous'),
                                            ('subtitle', 'Glabrous'),
                                            ('text', 'no hairs or pubescence')])
def test_output_for_display_values(one_para_display_object, key, substring):
    out = one_para_display_object.format_single_para_display('glabrous')
    assert isinstance(out, dict)
    helper.assert_in_string(out[key], substring)
