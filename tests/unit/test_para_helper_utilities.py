'''Tests for methods in helpers/no_import_common_class/utilities.py'''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

import pytest
import helpers.no_import_common_class.paragraph_helpers as helpers
import utilities.random_methods as utils
import testing.data.dict_constants as constants


def test_find_dictionary_from_list_by_key_and_value():
    cats = constants.LIST_OF_SIMILAR_DICTIONARIES
    black_cats = utils.find_dictionary_from_list_by_key_and_value(cats, 'color', 'black')
    assert len(black_cats) == 2
    assert black_cats[0]['color'] == 'black'
    assert black_cats[1]['color'] == 'black'


def test_find_value_from_dictionary_list():
    cats = constants.LIST_OF_DIFFERENT_DICTIONARIES
    current_cats = utils.find_value_from_dictionary_list(cats, 'alive')
    assert len(current_cats) == 2
    assert isinstance(current_cats[0], bool)
    assert current_cats[0]
    assert current_cats[1]


@pytest.mark.parametrize('key, expected', [('alive', True), ('name', False)])
def test_key_not_in_dictionary(key, expected):
    result = utils.key_not_in_dictionary({'name': 'Nemo'}, key)
    assert result == expected


@pytest.mark.parametrize('key, expected', [('alive', False), ('name', True)])
def test_key_in_dictionary(key, expected):
    result = utils.key_in_dictionary({'name': 'Nemo'}, key)
    assert result == expected


@pytest.mark.parametrize('key, expected', [('in_', True), ('in', True), ('file', False)])
def test_dictionary_key_begins_with_substring(key, expected):
    result = utils.dictionary_key_begins_with_substring({'in_file': 'data/input_file.json'}, key)
    assert result == expected


@pytest.mark.parametrize('key, value', [('name', 'Nemo'), ('color', 'black'), ('year', '1994')])
def test_dict_from_split_string(key, value):
    result = utils.dict_from_split_string('Nemo~black~1994', '~', ('name', 'color', 'year'))
    assert result[key] == value


@pytest.mark.parametrize('key_1, val_1, key_2, val_2_list, association_list', [
    ('dog_id', 'Inky', 'cat_id', ['Nemo', 'Grayface', 'PD'], None),
    ('dog_id', 'Camden', 'cat_id', ['Sammy', 'Mac'], [{'dog_id': 'Wrigley', 'cat_id': 'Sammy'},
                                                      {'dog_id': 'Wrigley', 'cat_id': 'Mac'}]),
    ('dog_id', 'Pluto', 'cat_id', ['Ninja', 'Ronin'], None)
])
def test_add_to_associations(key_1, val_1, key_2, val_2_list, association_list):
    size = 0 if association_list is None else len(association_list)
    resulting_list = helpers.add_to_associations(key_1, val_1, key_2, val_2_list, association_list)
    val_2 = val_2_list[-1]
    last_association = resulting_list[-1]
    assert len(resulting_list) == size + len(val_2_list)
    assert last_association[key_1] == val_1
    assert last_association[key_2] == val_2
