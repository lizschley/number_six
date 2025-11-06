import textwrap

FLAGS = {
    'modal': False,
    'table': False,
    'accordion': False,
}

FILES = {
    'input_file': 'basic_site_html/begin_html.html',
    'output_file': '/Users/eaffie/development/basic_website/liz/html/misc/carousel_testing.html',
    'data_file': 'basic_site_html/dr_brenner_gleanings.html',
}

END_HTML_VARIABLES = {
    'body_page_id': 'carousel_testing_page_id',
    'h1_id': 'carousel_testing_overview_h1',
    'h1_default_text': 'Carousel Testing',
    'main_container_id': 'carousel_testing_main_container',
    'h3_id': 'Hawaii',
    'h3_default_text': "2025 end of Sept trip to Hawaii",
    'begin_text': '',
}

# Pages with various options may need some extra imports
NEEDED_FOR_ACCORDION = [
    '      <link href="../../css/accordion.css" id="site_css" media="screen" rel="stylesheet"/>',
]

NEEDED_FOR_MODALS = [
    '      <script src="../../js/common_modal_new.js" defer type="text/javascript"></script>',
    '      <script src="../../data/misc_modals_new.js" defer type="text/javascript"></script>',
]

NEEDED_FOR_TABLE = [
    '      <script src="https://code.jquery.com/jquery-3.6.0.min.js" type="text/javascript" defer></script>',
    '      <script src="https://cdn.datatables.net/2.2.2/js/dataTables.js" type="text/javascript" defer></script>',
    '      <script src="../../js/plant_table.js" type="text/javascript" defer></script>',
]

END_TOP_HTML = textwrap.dedent(f'''\
           <title>Inquiries and Observations | Inquiries and Observations </title>
    </head>
    <body id='{END_HTML_VARIABLES['body_page_id']}'>
        <!-- Navbar -->
        <nav id='non_index_nav_id' class='navbar navbar-expand-sm fixed-top' aria-label='navbar'>
        </nav>
        <div id='header' class='clearfix' class='container-fluid'>
            <a href='../../../index.html' title='Home' rel='home' class='navbar-brand'>
                <img src='../../images/logo.png' class='img-fluid float-start' alt='cat logo, link to home'>
            </a>
            <div class='header_words'>
            <h1 id={END_HTML_VARIABLES['h1_id']}>{END_HTML_VARIABLES['h1_default_text']}</h1>
            </div>
        </div>
''')

TOP_END_HTML = textwrap.dedent(f'''\
        <div id='{END_HTML_VARIABLES['main_container_id']}' class='container-fluid px-5'>
            <h3 id='{END_HTML_VARIABLES['h3_id']}'>{END_HTML_VARIABLES['h3_default_text']}</h3>
            {END_HTML_VARIABLES['begin_text']}''')

END_HTML = textwrap.dedent('''\
    </body>
</html>
''')


# item_target needs numeral because it is repeatable and unique
# <div id="collapse1" class="accordion-collapse collapse" data-bs-parent="#philosophical_gleanings">
# target id needs to be preceded by '#collapse9', for example
# data-bs-toggle="collapse" data-bs-target="#collapse1" aria-expanded="false" aria-controls="collapse1"
ACCORDION_HTML_VARIABLES = {
    'parent_id': 'philosophical_gleanings',
    'index': 5,
    'orig_index': 5,
    'button_text': '',
    'body_lines': [],
    'wrote_header': False,
}

ACCORDION_HTML_TOP = textwrap.dedent(f'''\
            <div class="accordion" id="{ACCORDION_HTML_VARIABLES['parent_id']}">
''')

ACCORDION_HTML_BOTTOM = textwrap.dedent('''\
            </div>
''')

AWS_BEGIN_KEY = 'basic_website/travel/hawaii'

AWS_BEGIN_URL = f'https://lizschley-static.s3.us-east-1.amazonaws.com/{AWS_BEGIN_KEY}'

# these are the only variables needed (so far)
CAROUSEL_URLS = [
    f'{AWS_BEGIN_URL}/airplane_daytime.png',
    f'{AWS_BEGIN_URL}/airplane_sunrise.png']

CAROUSEL_DATA = {
    'urls': CAROUSEL_URLS,
    'carousel_id': 'airplane_carousel_id'
}

TOP_CAROUSEL_HTML = textwrap.dedent(f'''\
        <div id="{CAROUSEL_DATA['carousel_id']}" class="carousel slide">
            <div class="carousel-indicators">
    ''')

AFTER_CAROUSEL_INDICATORS = textwrap.dedent(f'''\
            </div>
            <div class="carousel-inner">
    ''')

BOTTOM_CAROUSEL_HTML = textwrap.dedent(f'''\
            </div>
            <button class="carousel-control-prev" type="button" data-bs-target="#{CAROUSEL_DATA['carousel_id']}" data-bs-slide="prev">
                <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Previous</span>
            </button>
            <button class="carousel-control-next" type="button" data-bs-target="#{CAROUSEL_DATA['carousel_id']}" data-bs-slide="next">
                <span class="carousel-control-next-icon" aria-hidden="true"></span>
                <span class="visually-hidden">Next</span>
            </button>
        </div>
    ''')
