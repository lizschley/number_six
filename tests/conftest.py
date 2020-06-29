'''This is location for session level fixtures.'''
# pylint: disable=missing-function-docstring
import pytest
import testing.constants.common as common


@pytest.fixture(scope='session')
def basic_paragraph_dict_file():
    '''Returns path to the basic paragraph json used for testing correct data.'''
    return common.BASIC_PARAGRAPH_TEST_JSON


@pytest.fixture
def basic_paragraph_dict_data(request):
    para_data = request.config.cache.get('basic_paragraph_input_dict/value', None)
    return para_data
