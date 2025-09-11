import textwrap


FLAGS = {
    'modal': False,
    'table': False,
}

FILES = {
    'input_file': 'basic_site_html/begin_html.html',
    'output_file': 'basic_site_html/plant_overview.html',
}

END_HTML_VARIABLES = {
    'body_page_id': 'plant_overview_page_id',
    'h1_id': 'plant_community_overview_h1',
    'h1_default_text': 'Plant Community Overview',
    'main_container_id': 'plant_community_main_container',
    'h3_id': 'plant_community_overview_h3',
    'h3_default_text': 'Plant Community Secondary Header',
    'default_text': 'Plant Community default text',
}

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

END_HTML = textwrap.dedent(f'''\
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
        <div id='{END_HTML_VARIABLES['main_container_id']}' class='container-fluid px-5'>
            <h3 id='{END_HTML_VARIABLES['h3_id']}'>{END_HTML_VARIABLES['h3_default_text']}</h3>
            <p>{END_HTML_VARIABLES['default_text']}</p>
        </div>
    </body>
</html>''')
