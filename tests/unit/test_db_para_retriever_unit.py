''' All tests only hit db_para_retriever, but the tests for test_db_output_to_display_input
hit many methods using dummy data.'''
# Todo: need to test coverage on the db_retriever methods
# pylint: disable=missing-function-docstring
import pytest
import testing.helpers.testing_helpers as helper
from common_classes.base_paragraph_retriever import BaseParagraphRetriever


def test_inheritance(db_para_retriever):
    assert issubclass(type(db_para_retriever), BaseParagraphRetriever)


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
    path = 'common_classes.db_paragraph_retriever.DbParagraphRetriever.'
    mocker.patch(path + 'write_sql')
    mock = mocker.patch(path + 'db_output_to_display_input')
    mock.return_value = {'test': 'test'}
    assert db_para_retriever.data_retrieval({'group_id': 1}) == {'test': 'test'}
    assert db_para_retriever.data_retrieval({}) is None


@pytest.mark.parametrize('substring', [('where g.id ='),
                                       ('paragraph_id'),
                                       ('link_text'),
                                       ('projects_group g'),
                                       ('projects_groupparagraph'),
                                       ('projects_paragraph'),
                                       ('reference'),
                                       ('projects_paragraphreference')])
def test_write_sql(db_para_retriever, substring):
    fullstring = db_para_retriever.write_sql()
    helper.assert_in_string(fullstring, substring)


def test_db_output_to_display_input(db_para_retriever, db_para_list_input):
    output_para = db_para_retriever.db_output_to_display_input(db_para_list_input)
    assert isinstance(output_para, dict)


@pytest.mark.parametrize('var_name, var_type', [('group', dict),
                                                ('paragraphs', list),
                                                ('references', list),
                                                ('para_id_to_link_text', dict)])
def test_db_output_keys(db_para_retriever, db_para_list_input, var_name, var_type):

    output_para = db_para_retriever.db_output_to_display_input(db_para_list_input)
    assert isinstance(output_para[var_name], var_type)