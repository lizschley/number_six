'''These fixtures are designed to be reused throughout tests.'''
# pylint: disable=missing-function-docstring
import pytest
import testing.helpers.testing_helpers as helpers


@pytest.fixture(scope='session')
def basic_para_dict_data(request):
    para_data = helpers.get_set_dict_from_json_cache(request)
    return para_data
