'''Unit tests for ParagraphDbInputCreator. '''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

from datetime import date

import pytest

import testing.data.string_constants as constants
import testing.helpers.testing_helpers as helper
from common_classes.paragraph_db_input_creator import ParagraphDbInputCreator
from portfolio.settings import BASE_DIR


@pytest.mark.parametrize('substring', [('data/data_for_creates/input_'),
                                       (BASE_DIR),
                                       ('.json'),
                                       (date.today().strftime('%Y-%m-%d'))])
def test_default_file_creation(substring):
    filepath = ParagraphDbInputCreator.create_json_file_path()
    print(filepath)
    helper.assert_in_string(filepath, substring)


def test_file_creation_prefix():
    filepath = ParagraphDbInputCreator.create_json_file_path(prefix=constants.FILE_PREFIX)
    print(filepath)
    helper.assert_in_string(filepath, constants.FILE_PREFIX)


def test_filename_creation_pass_in_filename():
    filepath = ParagraphDbInputCreator.create_json_file_path(filename=constants.FILENAME)
    print(filepath)
    helper.assert_in_string(filepath, constants.FILENAME)
