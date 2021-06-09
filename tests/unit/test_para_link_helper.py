'''Tests for methods in helpers/no_import_common_class/utilities.py'''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name

import pytest
from common_classes.para_link_helper import ParaLinkHelper
import testing.data.para_link_helper_kwargs as key_word_args
import testing.helpers.testing_helpers as helpers


@pytest.fixture()
def link_helper_modal_para_display():
    kwargs = key_word_args.KWARGS_LINK_HELPER_PARA_DISPLAY
    kwargs['create_modal_links'] = True
    link_helper = ParaLinkHelper(**kwargs)
    return link_helper


@pytest.fixture()
def link_helper_page_para_display():
    kwargs = key_word_args.KWARGS_LINK_HELPER_PARA_DISPLAY
    kwargs['create_modal_links'] = False
    link_helper = ParaLinkHelper(**kwargs)
    return link_helper


@pytest.fixture()
def link_helper_db_retriever():
    kwargs = key_word_args.KWARGS_LINK_HELPER_DB_RETRIEVER
    link_helper = ParaLinkHelper(**kwargs)
    return link_helper


@pytest.fixture()
def link_helper_slug_update():
    kwargs = key_word_args.KWARGS_LINK_HELPER_SLUG_UPDATE
    link_helper = ParaLinkHelper(**kwargs)
    return link_helper


def test_no_input_key_throws_value_error():
    kwargs = {'random': 'random'}
    with pytest.raises(ValueError):
        ParaLinkHelper(**kwargs)


def test_wrong_input_key_throws_value_error():
    kwargs = {'input_key': 'random'}
    with pytest.raises(ValueError):
        ParaLinkHelper(**kwargs)


def test_init_links_para_display_modal(link_helper_modal_para_display):
    assert link_helper_modal_para_display.input_data['create_modal_links']
    assert link_helper_modal_para_display.input_data['input_key'] == 'para_display'
    assert link_helper_modal_para_display.input_data['slug_data'] is None
    helpers.assert_link_helper_return_data(link_helper_modal_para_display)


def test_init_links_para_display_page(link_helper_page_para_display):
    assert not link_helper_page_para_display.input_data['create_modal_links']
    assert link_helper_page_para_display.input_data['input_key'] == 'para_display'
    assert link_helper_page_para_display.input_data['slug_data'] is None
    helpers.assert_link_helper_return_data(link_helper_page_para_display)


def test_init_links_db_retriever(link_helper_db_retriever):
    assert not link_helper_db_retriever.input_data['create_modal_links']
    assert link_helper_db_retriever.input_data['input_key'] == 'db_retriever'
    assert link_helper_db_retriever.input_data['slug_data'] is None
    helpers.assert_link_helper_return_data(link_helper_db_retriever)


def test_init_links_slug_update(link_helper_slug_update):
    assert not link_helper_slug_update.input_data['create_modal_links']
    assert link_helper_slug_update.input_data['input_key'] == 'slug_update'
    assert link_helper_slug_update.input_data['slug_data']['existing_slug'] == 'existing_slug'
    assert link_helper_slug_update.input_data['slug_data']['new_slug'] == 'new_slug'
    assert link_helper_slug_update.return_data['text'] == ''
    assert link_helper_slug_update.return_data['para_slugs'] is None
    assert link_helper_slug_update.return_data['group_slugs'] is None
