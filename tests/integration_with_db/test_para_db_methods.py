''' This will test the crud methods.'''
# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: pylint: disable=unused-import

import uuid
import pytest
from django.utils.text import slugify
from common_classes.para_db_methods import ParaDbMethods
import testing.data.create_input as data
from projects.models.paragraphs import (Category, Reference, Paragraph, Group,  # noqa: F401
                                        GroupParagraph, ParagraphReference)  # noqa: F401
from utilities.record_dictionary_utility import RecordDictionaryUtility


@pytest.fixture(scope='module')
def para_crud_methods():
    crud_methods = ParaDbMethods(updating=True)
    return crud_methods


@pytest.fixture()
def existing_para(para_crud_methods):
    create_dict = data.CREATE_PARA_WITHOUT_GUID
    create_dict['guid'] = str(uuid.uuid4())
    new_para = para_crud_methods.create_record(Paragraph,
                                               create_dict)
    return new_para


@pytest.fixture()
def different_standalone(para_crud_methods):
    create_dict = data.CREATE_PARA_WITHOUT_GUID
    create_dict['guid'] = str(uuid.uuid4())
    create_dict['subtitle'] = 'new and different'
    new_para = para_crud_methods.create_record(Paragraph,
                                               create_dict)
    return new_para


@pytest.fixture()
def not_standalone(para_crud_methods):
    create_dict = data.CREATE_PARA_WITHOUT_GUID
    create_dict['guid'] = str(uuid.uuid4())
    create_dict['subtitle'] = ''
    create_dict['standalone'] = False
    new_para = para_crud_methods.create_record(Paragraph,
                                               create_dict)
    return new_para


@pytest.mark.django_db
def test_auto_slug_will_create_slug(para_crud_methods) -> None:
    auto_slug_group = para_crud_methods.find_or_create_record(Group,
                                                              data.FIND_GROUP_AUTO_SLUG,
                                                              data.CREATE_GROUP_AUTO_SLUG)
    assert auto_slug_group['record'].slug == slugify(auto_slug_group['record'].title)


@pytest.mark.django_db
def test_auto_slug_will_not_override_input_data(para_crud_methods) -> None:
    input_slug_group = para_crud_methods.find_or_create_record(Group,
                                                               data.FIND_GROUP_WITH_SLUG,
                                                               data.CREATE_GROUP_WITH_SLUG)
    assert input_slug_group['record'].slug != slugify(input_slug_group['record'].title)


@pytest.mark.django_db
def test_rollback_happens(para_crud_methods) -> None:
    try:
        para_crud_methods.find_record(Group, data.FIND_GROUP_AUTO_SLUG)
        assert False
    except Group.DoesNotExist:
        assert True


@pytest.mark.django_db
def test_input_data_used_as_para_guid(para_crud_methods) -> None:
    find_dict = data.FIND_PARA_WITH_GUID
    create_dict = data.CREATE_PARA_WITHOUT_GUID
    para_guid = str(uuid.uuid4())
    find_dict['guid'] = para_guid
    create_dict['guid'] = para_guid
    new_para = para_crud_methods.find_or_create_record(Paragraph,
                                                       find_dict,
                                                       create_dict)
    assert new_para['record'].guid == para_guid


@pytest.mark.django_db
def test_input_unique_subtitle_for_standalone_para(para_crud_methods, existing_para) -> None:
    queryset = RecordDictionaryUtility.get_content(Paragraph, existing_para.id)
    update_dict = {}
    update_dict['id'] = queryset[0]['id']
    update_dict['guid'] = queryset[0]['guid']
    update_dict['subtitle'] = 'strange and wonderful data'
    find_dict = {'guid': queryset[0]['guid']}
    ret_dict = para_crud_methods.find_and_update_record(Paragraph, find_dict, update_dict)
    assert ret_dict['subtitle'] == update_dict['subtitle']


@pytest.mark.django_db
def test_successful_update_to_standalone_para(para_crud_methods, not_standalone) -> None:
    queryset = RecordDictionaryUtility.get_content(Paragraph, not_standalone.id)
    saved_updated_at = queryset[0]['updated_at']
    update_dict = {}
    update_dict['id'] = queryset[0]['id']
    update_dict['guid'] = queryset[0]['guid']
    update_dict['subtitle'] = 'strange and wonderful data'
    update_dict['standalone'] = True
    find_dict = {'guid': queryset[0]['guid']}
    ret_dict = para_crud_methods.find_and_update_record(Paragraph, find_dict, update_dict)
    assert ret_dict['subtitle'] == update_dict['subtitle']
    assert ret_dict['standalone'] == update_dict['standalone']
    assert ret_dict['updated_at'] > saved_updated_at


@pytest.mark.django_db
def test_update_successful_to_not_standalone_no_subtitle(para_crud_methods, existing_para) -> None:
    queryset = RecordDictionaryUtility.get_content(Paragraph, existing_para.id)
    update_dict = {}
    update_dict['id'] = queryset[0]['id']
    update_dict['guid'] = queryset[0]['guid']
    update_dict['subtitle'] = ''
    update_dict['standalone'] = False
    find_dict = {'guid': queryset[0]['guid']}
    ret_dict = para_crud_methods.find_and_update_record(Paragraph, find_dict, update_dict)
    assert ret_dict['subtitle'] == update_dict['subtitle']
    assert ret_dict['standalone'] == update_dict['standalone']


@pytest.mark.django_db
def test_error_standalone_changes_no_subtitle(para_crud_methods, not_standalone) -> None:
    queryset = RecordDictionaryUtility.get_content(Paragraph, not_standalone.id)
    update_dict = {}
    update_dict['id'] = queryset[0]['id']
    update_dict['guid'] = queryset[0]['guid']
    update_dict['standalone'] = True
    find_dict = {'guid': queryset[0]['guid']}
    ret_dict = para_crud_methods.find_and_update_record(Paragraph, find_dict, update_dict)
    assert 'error' in ret_dict.keys()
    assert 'Invalid paragraph!' in ret_dict['error']


@pytest.mark.skip(reason='Need to turn this into unit test')
@pytest.mark.django_db
def test_error_standalone_subtitle_removed(para_crud_methods, existing_para) -> None:
    queryset = RecordDictionaryUtility.get_content(Paragraph, existing_para.id)
    update_dict = {}
    update_dict['id'] = queryset[0]['id']
    update_dict['guid'] = queryset[0]['guid']
    update_dict['subtitle'] = ''
    find_dict = {'guid': queryset[0]['guid']}
    ret_dict = para_crud_methods.find_and_update_record(Paragraph, find_dict, update_dict)
    assert 'error' in ret_dict.keys()
    assert 'Invalid paragraph!' in ret_dict['error']


@pytest.mark.skip(reason='Need to turn this into unit test')
@pytest.mark.django_db
def test_error_standalone_non_unique_subtitle_edit(para_crud_methods, existing_para,
                                                   different_standalone):
    queryset = RecordDictionaryUtility.get_content(Paragraph, existing_para.id)
    update_dict = {}
    update_dict['id'] = queryset[0]['id']
    update_dict['guid'] = queryset[0]['guid']
    update_dict['subtitle'] = different_standalone.subtitle
    find_dict = {'guid': queryset[0]['guid']}
    ret_dict = para_crud_methods.find_and_update_record(Paragraph, find_dict, update_dict)
    assert 'error' in ret_dict.keys()
    assert 'Invalid paragraph!' in ret_dict['error']
