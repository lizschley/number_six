'''These fixtures are designed to be reused throughout tests.'''
# pylint: disable=missing-function-docstring
import pytest
import testing.helpers.testing_helpers as helpers
import testing.constants.common as common
import testing.data.dict_constants as constants


@pytest.fixture(scope='session')
def orig_para_dict_data(request):
    para_data = helpers.get_set_dict_from_json_cache(request)
    return para_data


@pytest.fixture(scope='session')
def display_text_from_json(request):
    display_data = helpers.get_set_display_para_from_json_cache(request)
    return display_data


@pytest.fixture(scope='session')
def json_path(request):
    return common.BASIC_PARA_TEST_JSON
