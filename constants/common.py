'''These are constants that will be used either for validation, processing or both'''
EXCLUDE_FROM_STUDY_GROUPS = ['Botany Definitions']
ORDER_FIELD_FOR_PARAS = 'order'
VALID_DATA_RETRIEVAL_ARGS = ('group_id', 'path_to_json', 'subtitle', 'category_id')
VALID_DB_RETRIEVER_KW_ARGS = ('group_id', 'search_str', 'subtitle')
SUBTITLE = 'subtitle'

# Note no spaces in div_ids, will do a replace space with _ to turn the link text into div_id
# https://stackoverflow.com/questions/441018/replacing-spaces-with-underscores-in-javascript
EXERCISE_GROUP_IDENTIFIERS = {'stretch-overview': 'Stretch Overview',
                              'animalistic-exercises': 'Animalistic',
                              'warmup': 'Warmup'}
