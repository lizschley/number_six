'''Common code for tests'''
# pylint: disable=missing-function-docstring
import helpers.import_common_class.paragraph_helpers as import_class_para_helper
import utilities.json_methods as json_helper
import testing.constants.common as common
import testing.data.dict_constants as data
from testing.data.row import Row


def get_set_dict_from_json_cache(request, path=common.BASIC_PARA_TEST_JSON,
                                 key=common.BASIC_PARA_DICT_KEY):
    return_dict = request.config.cache.get(key, None)
    if not return_dict:
        return_dict = json_helper.json_to_dict(path)
        request.config.cache.set(key, return_dict)
    return return_dict


def get_set_display_para_from_json_cache(request, path=common.BASIC_PARA_TEST_JSON,
                                         key=common.DISPLAY_PARA_DICT_KEY):
    return_dict = request.config.cache.get(key, None)
    if not return_dict:
        return_dict = import_class_para_helper.paragraph_list_from_json(path)
        request.config.cache.set(key, return_dict)
    return return_dict


def assert_instance_variable(obj, var_name, var_type):
    assert isinstance(getattr(obj, var_name), var_type)


def assert_in_string(fullstring, substring):
    assert substring in fullstring


def assert_not_in_string(fullstring, substring):
    assert substring not in fullstring


def assert_key_in_dictionary(test_dictionary, key):
    assert key in test_dictionary


def assert_key_not_in_dictionary(test_dictionary, key):
    assert key not in test_dictionary


def assert_link_helper_return_data(obj):
    assert obj.return_data['text'] == ''
    assert obj.return_data['para_slugs'] == []
    assert obj.return_data['group_slugs'] == []


def create_basic_para_raw_queryset_data():
    out_list = []
    start_data = data.PARA_DISPLAY_DB_INPUT_DATA_FOR_TESTING
    group_title = start_data['group_title']
    group_note = start_data['group_note']
    group_type = start_data['group_type']
    paras = start_data['paragraphs']
    for para in paras:
        out_list.append(create_row(group_title, group_note, group_type, para))
    return out_list


def create_row(group_title, group_note, group_type, para):
    return Row(group_title=group_title,
               group_note=group_note,
               group_type=group_type,
               paragraph_id=para['paragraph_id'],
               order=para['order'],
               subtitle=para['subtitle'],
               subtitle_note=para['subtitle_note'],
               image_path='',
               image_info_key=para['image_info_key'],
               text=para['text'],
               para_slug=para['para_slug'],
               short_title=para['short_title'],
               reference_id=para['reference_id'],
               link_text=para['link_text'],
               url=para['url'],
               short_text=para['short_text'],
               ref_slug=para['slug'])
