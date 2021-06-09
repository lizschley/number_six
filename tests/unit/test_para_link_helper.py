'''Tests for methods in helpers/no_import_common_class/utilities.py'''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

import pytest

@pytest.fixture()
def para_link_helper_object():
    paragraph = ParaLinkHelper()
    paragraph.input_data = constants.PARA_DISPLAY_ONE_PARA_INPUT
    return paragraph

@pytest.fixture()
def para_link_helper_object():
    paragraph = ParaLinkHelper()
    paragraph.input_data = constants.PARA_DISPLAY_ONE_PARA_INPUT
    return paragraph

@pytest.fixture()
def para_link_helper_object():
    paragraph = ParaLinkHelper()
    paragraph.input_data = constants.PARA_DISPLAY_ONE_PARA_INPUT
    return paragraph



def test_find_dictionary_from_list_by_key_and_value():
    cats = constants.LIST_OF_SIMILAR_DICTIONARIES
    black_cats = utils.find_dictionary_from_list_by_key_and_value(cats, 'color', 'black')
    assert len(black_cats) == 2
    assert black_cats[0]['color'] == 'black'
    assert black_cats[1]['color'] == 'black'