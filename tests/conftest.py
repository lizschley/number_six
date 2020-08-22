'''These fixtures are designed to be reused throughout tests.'''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
import pytest
import testing.helpers.testing_helpers as helper
import testing.constants.common as common
from common_classes.paragraphs_for_display import ParagraphsForDisplay
from common_classes.para_display_retriever_db import ParaDisplayRetrieverDb


@pytest.fixture(scope='session')
def orig_para_dict_data(request):
    para_data = helper.get_set_dict_from_json_cache(request)
    return para_data


@pytest.fixture(scope='session')
def display_text_from_json(request):
    return helper.get_set_display_para_from_json_cache(request)


@pytest.fixture(scope='session')
def db_para_list_input():
    return helper.create_basic_para_raw_queryset_data()


@pytest.fixture(scope='session')
def json_path(request):
    return common.BASIC_PARA_TEST_JSON


@pytest.fixture()
def para_for_display_object():
    paragraphs = ParagraphsForDisplay()
    return paragraphs


@pytest.fixture()
def db_para_retriever():
    retriever = ParaDisplayRetrieverDb()
    return retriever


@pytest.fixture()
def retriever_db_output(db_para_retriever, db_para_list_input):
    return db_para_retriever.db_output_to_display_input(db_para_list_input)
