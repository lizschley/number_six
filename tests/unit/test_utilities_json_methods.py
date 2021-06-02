'''Unit tests for ParagraphDbInputCreator. '''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

from datetime import date

import pytest

import testing.data.string_constants as constants
import testing.helpers.testing_helpers as helper
from portfolio.settings import BASE_DIR
from utilities import json_methods

@pytest.mark.parametrize('substring', [('data/data_for_creates/input_'),
                                       (BASE_DIR),
                                       ('.json'),
                                       (date.today().strftime('%Y-%m-%d'))])
def test_default_file_creation(substring):
    filepath = json_methods.create_json_file_path()
    print(filepath)
    helper.assert_in_string(filepath, substring)


def test_file_creation_prefix():
    filepath = json_methods.create_json_file_path(prefix=constants.FILE_PREFIX)
    print(filepath)
    helper.assert_in_string(filepath, constants.FILE_PREFIX)


def test_filename_creation_pass_in_filename():
    filepath = json_methods.create_json_file_path(filename=constants.FILENAME)
    print(filepath)
    helper.assert_in_string(filepath, constants.FILENAME)
