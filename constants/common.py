''' These are constants that will be used either for validation, processing or both '''
ORDER_FIELD_FOR_PARAS = 'order'
VALID_DATA_RETRIEVAL_ARGS = ('group_id', 'group_slug', 'path_to_json',
                             'category_id', 'category_slug', 'search_term')
VALID_DB_RETRIEVER_KW_ARGS = ('group_id', 'search_str', 'group_slug')
VALID_CAT_RETRIEVER_ARGS = ('category_id', 'category_slug')
VALID_SEARCH_RETRIEVER_ARGS = ('search_term')

''' These are constants that will be used for automating static files to reduce caching issues '''

PROD_VERSION_KEY = 'production_versions'
DEV_VERSION_KEY = 'development_versions'

STATIC_FILE_KEYS = ('css', 'flashcard', 'script', 'cat')

JSON_EXT = 'json'

EXPECTED_GET_VARIABLES = ['standalone', 'flashcard', 'ordered', 'search']
