'''class used in formatting various and consistant links within the paragraph text'''
from django.urls import reverse
import constants.para_lookup as lookup


class ParaLinkHelper:
    '''
    ParaLinkHelper allows convvenient and flexible inline links in the paragraph records.  This does not
    include references, unless they are used within the paragraph text)
    '''
    def __init__(self, replacing_text=True, create_modal_links=True):
        self.replacing_text = replacing_text
        self.create_modal_links = create_modal_links
        self.link_data = {}
        self.return_data = {'text': '', 'para_slugs': [], 'group_slugs': []}
        self.text = ''

    def links_from_indicators(self, text, link_data):
        '''
        links_from_indicators replaces all the link indicators with actual links or simply parses
        out the slugs to be used to retrieve the link data

        :param text: This is the text for a given text field in a paragraph record
        :type text: str
        :param link_data: this is all the link information needed to create the links in the paragraph
        :type link_data: dict
        :return: Either lists of slugs or paragraph text with html links instead of slugs & indicators
        :rtype: dict
        '''
        self.text = text
        self.link_data = link_data
        for indicator in lookup.INDICATOR_ARGS:
            self.loop_through_text(indicator['beg_link'], indicator['end_link'])
        return self.return_data

    def loop_through_text(self, beg_link, end_link):
        '''
        loop_through_text loops through the text field, which is split into an array of pieces.  For the
        split variable it uses the link indicators that enclose a slug.  The slug is used for the link
        data lookup.

        The result is added to self.return_data

        There are two goals:
        1. Parsing out the slugs, so we can retrieve the data necessary for creating the links.  This
           is preliminary to retrieving the link data.  Data retrieval is done in ParaDisplayRetrieverDb

        2. Parsing out the slugs, so we can use them as lookup keys (see step 1) to get the data
           necessary for the links.  In this step, we replace the parsed indicators and slugs with html
           links of various kinds. The html links are used for display, this step is performed within
           ParagraphsForDisplay processing.

        This link strategy offers convenience in writing a variety of link types: internal links to
        a single paragraph record, a group of ordered paragraphs, or a modal popup for a single
        paragraph or an external link.  It also ensures consistency of the links.

        :param beg_link
        :type str
        :param end_link
        :type str
        '''
        para_piece_list = []
        pieces = self.text.split(beg_link)
        for piece in pieces:
            if end_link not in piece:
                if self.replacing_text:
                    para_piece_list.append(piece)
            else:
                sub_pieces = piece.split(end_link)
                slug = sub_pieces[0]
                if not self.replacing_text:
                    self.append_slug(slug, beg_link)
                    continue
                para_piece_list.append(self.lookup_link(slug, beg_link))
                if len(sub_pieces) > 1:
                    para_piece_list.append(sub_pieces[1])
        if self.replacing_text:
            self.return_data['text'] = ''.join(para_piece_list)
        else:
            self.make_slug_list_unique()

    def append_slug(self, slug, beg_link):
        '''
        append_slug takes the slug that was between the link indicators and adds it to the slug array
        These links are used for inline links that actually link to another paragraph or group of
        paragraphs.  This is used to create the link data needed to create the links

        :param slug: slug found by looping through the paragraph and parsing it with the link indicators
        :type slug: string
        :param beg_link: one of the link indicators, need so we know if this is a para or a group link
        :type beg_link: string
        '''
        if beg_link in lookup.PARA_BEGIN:
            self.return_data['para_slugs'].append(slug)
        if beg_link == lookup.GROUP_ARGS['beg_link']:
            self.return_data['group_slugs'].append(slug)

    def lookup_link(self, slug, beg_link):
        '''
        lookup_link is where the methods that create the inline links are called

        :param slug: lookup key, to know which paragraph, group or reference is being called
        :type slug: string
        :param beg_link: used here to identify the kind of link needed
        :type beg_link: str
        :return: link to the paragraph, group or reference
        :rtype: str
        '''
        if (beg_link == lookup.AJAX_ARGS['beg_link'] and self.create_modal_links):
            return self.ajax_link(slug)
        if (beg_link == lookup.AJAX_ARGS['beg_link'] or beg_link == lookup.PARA_ARGS['beg_link']):
            return self.para_link(slug)
        if beg_link == lookup.REF_ARGS['beg_link']:
            return self.para_link(slug)
        if beg_link == lookup.GROUP_ARGS['beg_link']:
            return self.group_link(slug)
        return ''

    def ajax_link(self, slug):
        '''
        ajax_link This creates an ajax link: looks up single para by slug and displays result in modal

        :param orig_subtitle: This will be the link text, though it may not be the actual subtitle
        :type orig_subtitle: str
        :param from_ajax: True if displaying text that has link indicators - avoiding links with modals
        :type from_ajax: bool
        :return: paragraph with link indicators turned into modal link or has link indicators stripped
        :rtype: dict
        '''
        link_text = self.link_data['para_slug_to_short_title'][slug]

        beg_link = '<a href="#" data-slug="'
        mid_link = '" class="para_by_subtitle modal_popup_link">'
        end_link = '</a>'
        return beg_link + slug + mid_link + link_text + end_link

    def para_link(self, slug):
        '''
        para_link are links to standalone paragraphs that are in modal links or
        can display as its own page

        :return: a link to the standalone para.
        :rtype: string
        '''
        link_text = self.link_data['para_slug_to_short_title'][slug]
        beg_link = '<a class="nav-link" href="'
        end_link = f'">{link_text}</a>'
        url = reverse('projects:study_para_by_slug', kwargs={"slug":  slug})
        return beg_link + url + end_link

    def ref_link(self, slug):
        '''
        ref_link creates a standard link to display in a para with a class of reference_link.

        :param slug: slug for the reference to use for lookup, so we have ability to update link_text
        :type slug: string
        :return: html link within text
        :rtype: string
        '''
        link_text = self.link_data['ref_slug_to_short_text'][slug]
        url = self.link_data['ref'][slug]['url']
        return f'<a href="{url}" class="reference_link" target="_blank">{link_text}</a>'

    def group_link(self, _slug):
        '''
        group_link is not implementd
        :return: empty string
        :rtype: string
        '''
        return ''

    def make_slug_list_unique(self):
        '''
        make_slug_list_unique ensures that records will not be retrieved multiple times
        '''
        for key in ('para_slugs', 'group_slugs'):
            slug_list = self.return_data[key]
            if len(slug_list) > 1:
                slug_list = list(dict.fromkeys(slug_list))
                self.return_data[key] = slug_list
