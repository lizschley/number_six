import helpers.no_import_common_class.paragraph_helpers as ph


def test_create_link():
    url: str = 'http://www.math.com/'
    link_text: str = 'Math'
    link: str = ph.create_link(url, link_text)
    assert link == '<a href="http://www.math.com/" target="_blank">Math</a>'
