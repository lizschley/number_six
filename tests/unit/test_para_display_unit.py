'''Unit tests for ParagraphsForDisplay.  Note - sometimes test multiple methods at a time'''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

import pytest
from common_classes.paragraphs_for_display import ParagraphsForDisplay
from common_classes.db_paragraph_retriever import DbParagraphRetriever
from common_classes.json_paragraph_retriever import JsonParagraphRetriever
import testing.data.dict_constants as constants


@pytest.fixture()
def para_display_input_data():
    return constants.PARA_DISPLAY_INPUT_DATA_FOR_TESTING


def test_retrieve_paragraphs_bad_input(mocker, para_for_display_object):
    path = 'common_classes.paragraphs_for_display.ParagraphsForDisplay.'
    mock1 = mocker.patch(path + 'retrieve_input_data')
    mock2 = mocker.patch(path + 'format_data_for_display')
    mock1.return_value = None
    mock2.return_value = {'test': 'test'}
    with pytest.raises(BaseException):
        assert para_for_display_object.retrieve_paragraphs(group_id=1)


def test_retrieve_paragraphs_group_id(mocker, para_for_display_object):
    path = 'common_classes.paragraphs_for_display.ParagraphsForDisplay.'
    mock1 = mocker.patch(path + 'retrieve_input_data')
    mock2 = mocker.patch(path + 'format_data_for_display')
    mock1.return_value = {'test': 'test'}
    mock2.return_value = {'test': 'test'}
    assert para_for_display_object.retrieve_paragraphs(group_id=1) == {'test': 'test'}


def test_para_display_init(para_for_display_object):
    assert isinstance(para_for_display_object.title, str)
    assert isinstance(para_for_display_object.title_note, str)
    assert isinstance(para_for_display_object.reference_links, dict)
    assert isinstance(para_for_display_object.paragraphs, list)
    assert isinstance(para_for_display_object.input_data, dict)


@pytest.mark.parametrize("key,expected", [('path_to_json', JsonParagraphRetriever),
                                          ('group_id', DbParagraphRetriever)])
def test_instantiate_class(key, expected):
    paragraphs = ParagraphsForDisplay()
    obj = paragraphs.instantiate_class(key)
    assert isinstance(obj, expected)


def test_instantiate_class_with_something_wrong(para_for_display_object):
    assert para_for_display_object.instantiate_class('something_wrong') is None


def test_assign_group_data(para_for_display_object, para_display_input_data):
    para_for_display_object.group = para_display_input_data['group']
    assert para_for_display_object.group['title'].strip() == 'Listening'
    assert para_for_display_object.group['note'].strip() == '*Note - subjects I listen to'


def test_create_links_from_references(para_for_display_object, para_display_input_data):
    para_for_display_object.input_data['references'] = para_display_input_data['references']
    para_for_display_object.create_links_from_references()
    ref_links = para_for_display_object.reference_links
    assert len(para_for_display_object.reference_links) == 2
    assert 'href="https://literature.org/"' in ref_links['Literature']
    assert 'href="https://gymcastic.com/"' in ref_links['JessicaSpencerKensley']


def test_assign_paragraphs(para_for_display_object, para_display_input_data):
    '''this also tests add_links_to_paragraphs and paragraph_links'''
    para_for_display_object.input_data = para_display_input_data
    para_for_display_object.create_links_from_references()
    para_for_display_object.assign_paragraphs()
    paras = para_for_display_object.paragraphs
    assert len(paras) == 2
    assert isinstance(paras[0]['references'], str)
    assert 'href=' in paras[0]['references']
    assert paras[1]['id'] == 'first'
    assert paras[1]['subtitle'] == 'Fiction'


def test_paragraph(para_display_input_data):
    para = para_display_input_data['paragraphs'][0]
    return_para = ParagraphsForDisplay.paragraph(para)
    assert isinstance(return_para, dict)
    assert return_para['id'] == para['id']
    assert return_para['subtitle'] == para['subtitle']
    assert return_para['text'] == para['text']
    assert return_para['references'] == ''


def test_output_for_display(para_for_display_object, para_display_input_data):
    para_for_display_object.title = para_display_input_data['group']['title']
    para_for_display_object.title_note = para_display_input_data['group']['note']
    para_for_display_object.paragraphs = para_display_input_data['paragraphs']
    out = para_for_display_object.output_for_display()
    assert out['title'] == para_display_input_data['group']['title']
    assert out['title_note'] == para_display_input_data['group']['note']
    assert isinstance(out['paragraphs'], list)
