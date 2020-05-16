
def start_with_data():
    # start with list of links
    reference_links = [
        {'link_text': 'bb', 'link': '<a href="https://balancebeamsituation.com/">bb</a>'},
        {'link_text': 'wwgym', 'link': '<a href="http://wwgym.com/forum/main-gymnastics-forums">ww</a>'},
        {'link_text': 'gymter', 'link': '<a href="https://thegymter.net/">gymternet</a>'},]


    # and paragraphs
    paragraphs = [{'id': '1', 'sub_title': 'subtitle 1', 'sub_title_note': '', 'text': 'Text 1', 'stand_alone': True, 'references': []},
                  {'id': '2', 'sub_title': 'subtitle 2', 'sub_title_note': '', 'text': 'Text 2', 'stand_alone': True, 'references': []},
                  {'id': '3', 'sub_title': 'subtitle 3', 'sub_title_note': '', 'text': 'Text 3', 'stand_alone': True, 'references': []},
    ]

    # and relationships
    ref_para = [
        {
          "link_text": "bb",
          "paragraph_id": "1"
        },
        {
          "link_text": "wwgym",
          "paragraph_id": "2"
        },
        {
          "link_text": "gymter",
          "paragraph_id": "2"
        },
        {
            "link_text": "gymter",
            "paragraph_id": "3"
        },
    ]
    paragraphs = add_links_to_paragraphs(paragraphs, ref_para, reference_links)
    print(paragraphs)


def add_links_to_paragraphs(paragraphs, ref_para, ref_links):
    for para in paragraphs:
        associations = list(filter(lambda par: para['id'] == par['paragraph_id'], ref_para))
        para['references'] = retrieve_paragraph_links(associations, ref_links)
    return paragraphs


def retrieve_paragraph_links(associations, ref_links):
    para_links = []
    for assoc in associations:
        print(assoc)
        links = list(filter(lambda link: assoc['link_text'] == link['link_text'], ref_links))
        para_links.append(links[0]['link'])
    return para_links


def test_scope():
    references = [{'url': 'http://wwgym.com/forum/main-gymnastics-forums/women-s-artistic-gymnastics',
                   'link_text': 'wwgym'},
                  {'url': 'https://balancebeamsituation.com/', 'link_text': 'bb situation'},]
    for ref in references:
        link = create_link(ref)
    print(link)


def create_link(ref):
    url = ref['url']
    link_text = ref['link_text']
    return f'<a href="{url}" target="_blank">{link_text}</a>'