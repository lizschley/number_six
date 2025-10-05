import textwrap

FLAGS = {
    'modal': False,
    'table': False,
    'accordion': True,
}

FILES = {
    'input_file': 'basic_site_html/begin_html.html',
    'output_file': '/Users/eaffie/development/basic_website/liz/html/misc/accordion_testing.html',
    'data_file': 'basic_site_html/dr_brenner_gleanings.html',
}

END_HTML_VARIABLES = {
    'body_page_id': 'accordion_testing_page_id',
    'h1_id': 'accordion_testing_overview_h1',
    'h1_default_text': 'Accordion Testing',
    'main_container_id': 'accordion_testing_main_container',
    'h3_id': 'blog_intro_h3',
    'h3_default_text': "Dr Brenner's Gleanings",
    'begin_text': '<p>Compiled by Dr William H Brenner with references indicated informally</p>',
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
        </div>''')

TOP_END_HTML = textwrap.dedent(f'''\
        <div id='{END_HTML_VARIABLES['main_container_id']}' class='container-fluid px-5'>
            <h3 id='{END_HTML_VARIABLES['h3_id']}'>{END_HTML_VARIABLES['h3_default_text']}</h3>
            <p>{END_HTML_VARIABLES['begin_text']}</p>
        </div>''')

END_HTML = textwrap.dedent('''\
    </body>
</html>''')


# accordion_item_target_id needs numeral because it is repeatable and unique
# <div id="collapse1" class="accordion-collapse collapse" data-bs-parent="#philosophical_gleanings">
# target id needs to be preceded by '#collapse9', for example
# data-bs-toggle="collapse" data-bs-target="#collapse1" aria-expanded="false" aria-controls="collapse1"
ACCORDION_HTML_VARIABLES = {
    'parent_id': 'philosophical_gleanings',
    'blockquote_class': 'accordion_indent',
    'accordion_item_target_id': 'collapse',
    'rep_var': {
        'index': 5,
        'button_text': '',
        'ready_for_item_lines': False,
        'end_prior_repeatable': False,
    }
}

ACCORDION_HTML_TOP = textwrap.dedent(f'''\
             <div class="accordion" id="{ACCORDION_HTML_VARIABLES['parent_id']}">''')

# ACCORDION_BUTTON_TOP & ACCORDION_ITEM_DIV are used to create the ACCORDIAN_REPEATABLE_HTML
# This is only possible if we can seed the last index and we know the button text
ACCORDION_BUTTON_TOP = "<button class='accordion-button collapsed' type='button' data-bs-toggle='"
ACCORDION_BUTTON_TOP += f"{ACCORDION_HTML_VARIABLES['accordion_item_target_id']}' data-bs-target='"
ACCORDION_BUTTON_TOP += f"#{ACCORDION_HTML_VARIABLES['accordion_item_target_id']}'"
ACCORDION_BUTTON_TOP += f"{ACCORDION_HTML_VARIABLES['rep_var']['index']} aria-expanded='false' "
ACCORDION_BUTTON_TOP += "aria-controls='"
ACCORDION_BUTTON_TOP += f"{ACCORDION_HTML_VARIABLES['accordion_item_target_id']}"
ACCORDION_BUTTON_TOP += f"{ACCORDION_HTML_VARIABLES['rep_var']['index']}'>"

ACCORDION_ITEM_DIV = '<div id=' + f"{ACCORDION_HTML_VARIABLES['accordion_item_target_id']}"
ACCORDION_ITEM_DIV += f"{ACCORDION_HTML_VARIABLES['rep_var']['index']}"
ACCORDION_ITEM_DIV += "class='accordion-collapse collapse' "
ACCORDION_ITEM_DIV += f"data-bs-parent='#{ACCORDION_HTML_VARIABLES['parent_id']}'>"


ACCORDION_REPEATABLE_HTML = textwrap.dedent(f'''\
                <div class="accordion-item">
                <h2 class="accordion-header">
                    {ACCORDION_BUTTON_TOP}
                    {ACCORDION_HTML_VARIABLES['rep_var']['button_text']}
                    </button>
                </h2>
                {ACCORDION_ITEM_DIV}
                    <div class="accordion-body">''')

ACCORDIAN_END_REPEATABLE = textwrap.dedent('''\
                    </div>
                </div>
                </div>''')


ACCORDION_BOTTOM_HTML = textwrap.dedent('''\
            </div>
        </div>''')
