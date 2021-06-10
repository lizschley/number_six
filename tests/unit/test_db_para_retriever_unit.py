''' All tests only hit db_para_retriever, but the tests for test_db_output_to_display_input
hit many methods using dummy data.'''
# Todo: need to test coverage on the db_retriever methods
# pylint: disable=missing-function-docstring
import pytest

import testing.helpers.testing_helpers as helper
from common_classes.para_display_retriever_base import ParaDisplayRetrieverBase


def test_inheritance(db_para_retriever):
    assert issubclass(type(db_para_retriever), ParaDisplayRetrieverBase)


@pytest.mark.parametrize('var_name, var_type', [('ordered', bool),
                                                ('para_ids', list),
                                                ('ref_ids', list),
                                                ('group', dict),
                                                ('para_id_to_link_text', dict),
                                                ('paragraphs', list),
                                                ('references', list)])
def test_para_retriever_init(db_para_retriever, var_name, var_type):
    helper.assert_instance_variable(db_para_retriever, var_name, var_type)


def test_data_retrieval(mocker, db_para_retriever):
    path = 'common_classes.para_display_retriever_db.ParaDisplayRetrieverDb.'
    mocker.patch(path + 'write_group_para_sql')
    mock = mocker.patch(path + 'db_output_to_display_input')
    mock.return_value = {'test': 'test'}
    assert db_para_retriever.data_retrieval({'group_id': 1}) == {'test': 'test'}


@pytest.mark.parametrize('substring', [('where g.id ='),
                                       ('title'),
                                       ('title_note'),
                                       ('paragraph_id'),
                                       ('link_text'),
                                       ('projects_group g'),
                                       ('projects_groupparagraph'),
                                       ('projects_paragraph'),
                                       ('reference'),
                                       ('projects_paragraphreference')])
def test_write_group_para_sql(db_para_retriever, substring):
    fullstring = db_para_retriever.write_group_para_sql('group_id')
    helper.assert_in_string(fullstring, substring)


@pytest.mark.parametrize('substring', [('where p.slug ='),
                                       ('paragraph_id'),
                                       ('link_text'),
                                       ('projects_paragraph'),
                                       ('reference'),
                                       ('projects_paragraphreference'),
                                       ('title'),
                                       ('title_note')])
def test_write_one_standalone_para_sql(db_para_retriever, substring):
    fullstring = db_para_retriever.write_one_standalone_para_sql()
    helper.assert_in_string(fullstring, substring)


@pytest.mark.parametrize('substring', [('where g.id ='),
                                       ('projects_group g'),
                                       ('projects_groupparagraph')])
def test_no_group_in_only_standalone_para_sql(db_para_retriever, substring):
    fullstring = db_para_retriever.write_one_standalone_para_sql()
    helper.assert_not_in_string(fullstring, substring)


def test_db_output_to_display_input(retriever_db_output):
    assert isinstance(retriever_db_output, dict)


@pytest.mark.parametrize('var_name, var_type', [('group', dict),
                                                ('paragraphs', list),
                                                ('references', list),
                                                ('para_id_to_link_text', dict)])
def test_db_output_keys(retriever_db_output, var_name, var_type):
    assert isinstance(retriever_db_output[var_name], var_type)


@pytest.mark.parametrize('var_name, var_length', [('group', 3),
                                                  ('paragraphs', 2),
                                                  ('references', 2),
                                                  ('para_id_to_link_text', 2)])
def test_db_output_length_correct(retriever_db_output, var_name, var_length):
    assert len(retriever_db_output[var_name]) == var_length


@pytest.mark.parametrize('outer, idx, inner, substring', [('paragraphs', 0, 'order', 'iction'),
                                                          ('paragraphs', 0, 'subtitle', 'iction'),
                                                          ('paragraphs', 0, 'text', 'non-domestic'),
                                                          ('references', 0, 'link_text', 'Lit'),
                                                          ('references', 0, 'url', 'lit'),
                                                          ('paragraphs', 1, 'order', 'annoying'),
                                                          ('paragraphs', 1, 'subtitle', 'annoying'),
                                                          ('paragraphs', 1, 'text', 'my cats'),
                                                          ('references', 1, 'link_text', 'Spencer'),
                                                          ('references', 1, 'url', 'gymcastic')])
def test_db_output_list_data_values_correct(retriever_db_output, outer, idx, inner, substring):
    helper.assert_in_string(retriever_db_output[outer][idx][inner], substring)


@pytest.mark.parametrize('outer, key, substring', [('group', 'group_title', 'Listen'),
                                                   ('group', 'group_note', 'subjects')])
def test_db_output_dict_data_values_correct(retriever_db_output, outer, key, substring):
    helper.assert_in_string(retriever_db_output[outer][key], substring)


@pytest.mark.parametrize('outer, key, substring', [('para_id_to_link_text', 'first', 'itera'),
                                                   ('para_id_to_link_text', 'second', 'Spencer')])
def test_db_output_list_first_data_value_correct(retriever_db_output, outer, key, substring):
    helper.assert_in_string(retriever_db_output[outer][key][0], substring)
