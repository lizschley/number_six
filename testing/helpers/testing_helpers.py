'''Common code for tests'''
# pylint: disable=missing-function-docstring
import helpers.no_import_common_class.paragraph_helpers as para_helper
import testing.constants.common as common


def get_set_dict_from_json_cache(request, path=common.BASIC_PARA_TEST_JSON,
                                 key=common.BASIC_PARA_DICT_KEY):
    return_dict = request.config.cache.get(key, None)
    if not return_dict:
        return_dict = para_helper.json_to_dict(path)
        request.config.cache.set(key, return_dict)
    return return_dict