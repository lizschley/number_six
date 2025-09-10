import textwrap

MODAL = False
TABLE = False

# Pages with many modal options have separate data files
NEEDED_FOR_MODALS = [
    '<script src="../../js/common_modal_new.js" defer type="text/javascript"></script>',
    '<script src="../../data/misc_modals_new.js" defer type="text/javascript"></script>',
]

NEEDED_FOR_TABLE = [
    '<script src="https://code.jquery.com/jquery-3.6.0.min.js" type="text/javascript" defer></script>',
    '<script src="https://cdn.datatables.net/2.2.2/js/dataTables.js" type="text/javascript" defer></script>',
    '<script src="../../js/plant_table.js" type="text/javascript" defer></script>',
]

END_HTML_VARIABLES = {
    'body_page_id': 'plant_overview_page_id',
    'h1_id': 'plant_community_overview_h1',
    'main_container_id': 'plant_community_main_container',
    'h3_id': 'plant_community_overview_h3',
    'default_text_id': 'plant_community_default_text',
}

FILES = {
    'input_file': 'basic_site_html/begin_html.html',
    'output_file': 'basic_site_html/plant_overview.html',
}


def files():
    file_list = []
    if MODAL:
        file_list = NEEDED_FOR_MODALS
    if TABLE:
        file_list = file_list + NEEDED_FOR_TABLE
    return file_list


def end_html():
    '''
        This is used for creating new pages. The html helps eliminate boring work and bugs, while eventually
        speeding up development on my basic website.

        Usage will be documented in scripts/name_of_script
    '''

    return textwrap.dedent(f'''\
        <title>Inquiries and Observations | Inquiries and Observations </title>
    </head>
    <body class='{END_HTML_VARIABLES['body_page_id']}'
        <!-- Navbar -->
        <nav id='non_index_nav_id' class='navbar navbar-expand-sm fixed-top' aria-label='navbar'>
        </nav>
        <div id='header' class='clearfix' class='container-fluid'>
            <a href='../../../index.html' title='Home' rel='home' class='navbar-brand'>
                <img src='../../images/logo.png' class='img-fluid float-start' alt='cat logo, link to home'>
            </a>
            <div class='header_words'>
            <h1>{END_HTML_VARIABLES['h1_id']}</h1>
            </div>
        </div>
        <div id='{END_HTML_VARIABLES['container_id']}' class='container-fluid px-5'>
            <h3 id='{END_HTML_VARIABLES['h3_id']}'>Overview</h3>
            <p>{END_HTML_VARIABLES['default_text']}</p>
        </div>
    </body>
</html>''')
