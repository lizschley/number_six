''' Constants used for albermarle county native plant db screen scraping '''

AC_NATIVE_PLANT_HEADERS = {
    0: 'Scientific/Common Name',
    1: 'Stormwater Facilities',
    2: 'Recommended Uses',
    3: 'Plant Needs',
    4: 'Plant Characteristics'
}

FIRST_DATA_IDX = 4

USDA_BASE_PLANT_URL = 'https://plants.usda.gov/core/profile?symbol='

AC_NATIVE_PLANT_URL = 'http://webapps.albemarle.org/NativePlants/list.asp?ShowAll=ALL'

AC_NATIVE_SUBTITLE_NOTE = ('Text was originally screen scraped from Albermarle County Organization\'s '
                           'Native Plant Database: '
                           '<a href="http://webapps.albemarle.org/NativePlants/list.asp?ShowAll=ALL" '
                           'class="reference_link" '
                           'target="_blank">Albemarle Native DB retrieved on 20210318</a> '
                           'The text here, has not been changed since.')

TEXT_KEYS = ('Type of Plant', 'Native Status', 'Leaves', 'Flowers', 'Size', 'Wildlife Value',
             'Caterpillars', 'Characteristics', 'Growing Conditions', 'Uses',
             'Stormwater Facilities')

TEXT_TEMPLATE = {
    'Leaves': [],
    'Native Status': [],
    'Flowers': [],
    'Type of Plant': [],
    'Size': [],
    'Wildlife Value': [],
    'Caterpillars': [],
    'Growing Conditions': [],
    'Stormwater Facilities': [],
    'Uses': [],
    'Characteristics': []
}

USES_LIST = ('Landscape', 'Horticulture', 'Erosion')

LOOKUP = {
    'Caterpillars': ['Cat. Comm Name:', 'Cat. Sci Name'],
    'Growing Conditions': ['Unique Soil'],
    'Plant Characteristics': ['Est', 'Foliage', 'Flower', 'Bloom']
}
