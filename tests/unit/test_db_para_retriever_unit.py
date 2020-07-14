''' Unit tests for the db_para_retriever '''
# pylint: disable=missing-function-docstring
import pytest
import testing.data.dict_constants as constants
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

def test_write_sql():
    pass


def test_basic_sql():
    pass


def test_db_output_to_display_input():
    pass


def test_loop_through_queryset():
    pass


def test_first_row_assignments():
    pass


def test_append_unique_reference():
    pass


def test_append_unique_paragraph():
    pass


def test_paragraph_dictionary():
    pass
