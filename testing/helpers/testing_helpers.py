'''Common code for tests'''
# pylint: disable=missing-function-docstring
import helpers.no_import_common_class.paragraph_helpers as para_helper
import testing.constants.common as common


def get_basic_para_cache(path, request):
    return_dict = request.config.cache.get(common.BASIC_PARA_DICT_KEY, None)
    if not return_dict:
        return_dict = para_helper.json_to_dict(path)
        request.config.cache.set(common.BASIC_PARA_DICT_KEY, return_dict)
    return return_dict
