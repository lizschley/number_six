import textwrap


FLAGS = {
    'modal': False,
    'table': False,
    'accordian': True,
}

FILES = {
    'input_file': 'basic_site_html/begin_html.html',
    'output_file': '/Users/eaffie/development/basic_website/liz/html/blog/test_using_blognbhn .html',
}

END_HTML_VARIABLES = {
    'body_page_id': 'blog_intro_page_id',
    'h1_id': 'blog_intro_overview_h1',
    'h1_default_text': 'Blog Introduction',
    'main_container_id': 'blog_intro_main_container',
    'h3_id': 'blog_intro_h3',
    'h3_default_text': 'Blog Introduction and Reason',
    'default_text': 'Begin here',
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
        <div id='{END_HTML_VARIABLES['main_container_id']}' class='container-fluid px-5'>
            <h3 id='{END_HTML_VARIABLES['h3_id']}'>{END_HTML_VARIABLES['h3_default_text']}</h3>
            <p>{END_HTML_VARIABLES['default_text']}</p>
        </div>''')


END_HTML = textwrap.dedent(f'''\
    </body>
</html>''')

ACCORDIAN_HTML = textwrap.dedent(f'''\
        <div id='tech_questions_and_answers' class='container-fluid px-5'>
            <h6>The following answers were accurate in late 2020:</h6>
            <div class="accordion" id="tech-q-and-a-id">
                <div class="accordion-item">
                <h2 class="accordion-header">
                    <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                    How do you add a Subdomain to a Letsencrypt Certificate?
                    </button>
                </h2>
                <div id="collapseOne" class="accordion-collapse collapse" data-bs-parent="#tech-q-and-a-id">
                    <div class="accordion-body">
                    <p>
                        When I accepted that in the real world you need to have a www subdomain, I was able to add it through AWS. I did not document that process, because AWS did a good job of explaining and it seemed to work perfectly. However, I later found out that it gave a security error in Safari. It said that my valid site may be spoofed. Therefore, I needed to add a www subdomain to my certificate.
                    </p>
                    <p>Ran this from <a href="https://technologytales.com/2019/06/11/adding-a-new-domain-or-subdomain-to-an-ssl-certificate-using-certbot/" class="reference_link" target="_blank">Technologytales 20190611</a>: </p>
                    <pre><code>&gt;&gt;&gt;sudo certbot --expand -d existing.com,www.example.com</code></pre>
                    It worked, but it broke the automatic redirect from www.domain.com to domain.com that worked before.  This is obviously an Apache problem, since www.domain.com brought up the default Apache page that lives on the server.
                    <p></p>
                    <p>This error was fixed by using advice from <a href="https://linuxize.com/post/redirect-http-to-https-in-apache/" class="reference_link" target="_blank">Linuxize 20200101</a>. I had to add their suggested code to two files (example.conf and example-le-ssl.conf). </p>
                    <p>Everything works, which is great, but someday, I would like to look at what I have with someone who understands Apache best practices.  Plus, I should test the fix again after the cron job renews the certificate.</p>
                    <h5>References</h5>
                    <a href="https://technologytales.com/2019/06/11/adding-a-new-domain-or-subdomain-to-an-ssl-certificate-using-certbot/" class="reference_link" target="_blank">Technologytales_20190611_AddingNewDomainSubdomain_SSL_Certificate_Certbot</a><br><a href="https://linuxize.com/post/redirect-http-to-https-in-apache/" class="reference_link" target="_blank">Linuxize_20200101_RedirectHttpHttpsApache</a><br>
                    </div>
                </div>
                </div>
            </div>
        </div>''')
