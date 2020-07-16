'''These fixtures are designed to be reused throughout tests.'''
# pylint: disable=missing-function-docstring
import pytest
import testing.helpers.testing_helpers as helper
import testing.constants.common as common
from common_classes.paragraphs_for_display import ParagraphsForDisplay
from common_classes.db_paragraph_retriever import DbParagraphRetriever


@pytest.fixture(scope='session')
def orig_para_dict_data(request):
    para_data = helper.get_set_dict_from_json_cache(request)
    return para_data


@pytest.fixture(scope='session')
def display_text_from_json(request):
    display_data = helper.get_set_display_para_from_json_cache(request)
    return display_data


@pytest.fixture(scope='session')
def json_path(request):
    return common.BASIC_PARA_TEST_JSON


@pytest.fixture()
def para_for_display_object():
    paragraphs = ParagraphsForDisplay()
    return paragraphs


@pytest.fixture()
def db_para_retriever():
    retriever = DbParagraphRetriever()
    return retriever


@pytest.fixture()
def db_para_list_input():
    db_data_list = helper.get_set_display_para_from_db_pickle()
    return db_data_list
