''' This class outputs a dictionary in a format used to display paragraphs.  It can be used
    for any page that either has only one group or that does not display by group.'''
import helpers.no_import_common_class.category_helpers as cat_helpers
from common_classes.paragraphs_for_display import ParagraphsForDisplay


class ParagraphsForDisplayCat(ParagraphsForDisplay):
    '''
    ParagraphsForDisplay is used to create the context for the paragraph display views

    Title and title_note are added directly to the context, whereas the reference links
    are turned into html code that are are links to references that are associated
    with each paragraph.  The paragraph list will also be added directly to the context.

    The input_data is a dictionary that is formatted by a paragraph retriever object.
    The plans are for different flavors of retrievers, based on the storage format.

    :param object: is formatted by a paragraph retriever object
    :type object: dictionary
    '''
    def __init__(self):
        super().__init__()
        # self.title = ''
        # self.reference_links = {}
        # self.input_data = {}

        # This is the output (along with the title)
        self.groups = []
        self.side_menu = ''
        self.hidden_flashcard_divs = ''

    def format_data_for_display(self):
        '''
        format_data_for_display Once we know what class to use for retrieving the input data
        this is the main driver for the formatting process

        :return: dictionary to be added to the context & used in the paragraph display template
        :rtype: dict
        '''
        if not self.input_data['category']:
            message = ('Your selection produced no results, please select something else or try '
                       'the same selection another day.')
            return self.output_error(message)
        self.assign_title()
        self.create_links_from_references()
        self.assign_groups()
        return self.output_for_display()

    def assign_title(self):
        '''
        assign_title, for example title; paragraph displayer has no concept of group
        '''
        category = self.input_data['category']
        self.title = '' if category['title'].strip() in ('resume') else category['title'].strip()

    def assign_groups(self):
        '''
        assign_groups takes each group input, as retrieved in the the category retriever and
        makes it work for the category display
        '''
        prefix = ''
        for data in self.input_data['groups']:
            group = data['group']
            group = self.assign_category_div_variables(group, prefix)
            prefix = '~' if self.is_flashcard() else '<br>'
            paragraphs = self.paragraphs_links_and_images(data['paragraphs'])
            ref_links = self.assign_ref_links(data['link_text'])
            self.groups.append(self.output_group(group, paragraphs, ref_links))

    def assign_ref_links(self, link_text_list):
        '''
        assign_ref_links formats the references for a given group

        :link_text_list: takes a list of the link_text associated with the current group
        :type link_text_list: list
        :return: list of the html links assoicated with the paragraph (separated with html new_line)
        :rtype: list of strings
        '''
        ref_links = ''
        for link_text in link_text_list:
            ref_links += self.reference_links[link_text] + '<br>'
        return ref_links

    @staticmethod
    def paragraph(para):
        '''
        paragraph is the format of a given paragraph expected in the paragraph display template

        :param para: one paragraph formatted as in input data
        :type para: dict
        :return: one paragraph formatted as needed in the paragraph display template
        :rtype: dict
        '''
        para = {
            'id': para['id'],
            'subtitle': para['subtitle'],
            'subtitle_note': para['note'],
            'text': para['text'],
            'image_path': para['image_path'],
            'image_classes': para['image_classes'],
            'image_alt': para['image_alt'],
        }
        return para

    def output_group(self, group, paragraphs, ref_links):
        '''
        output_group is the format that the category display expects for each group in the list of groups

        :param group: group fields
        :type group: dictionary
        :param paragraphs: List of paragraphs associated with the given group
        :type paragraphs: list of dictionaries
        :param ref_links: links in html format for the references
        :type ref_links: list of strings
        '''
        title = '' if group['note'].strip() == 'no-title-display' else group['title']
        cat_type = self.input_data['category']['category_type']
        if self.is_flashcard():
            title = 'Question: ' + title
            collapse_id = group['group_div_id'] + '_collapse'
            para_html = cat_helpers.flashcard_paragraph_layout(paragraphs, collapse_id, ref_links)
        else:
            para_html = cat_helpers.paragraphs_for_category_pages(paragraphs, cat_type)

        return {
            'title': title,
            'paragraphs': para_html,
            'group_div_id': group['group_div_id'],
            'group_div_class': group['group_div_class'],
            'ref_links': '' if self.is_flashcard() else ref_links}

    def output_for_display(self):
        '''
        output_for_display creates the **kwargs for the display paragraph template

        :return: final dict transformed in the study view to use in display paragraph template
        :rtype: dict
        '''
        display = {'title': self.title,
                   'groups': self.groups, }
        if self.is_flashcard():
            display['hidden_flashcard_divs'] = self.hidden_flashcard_divs
        else:
            display['side_menu'] = self.side_menu
        return display

    def is_flashcard(self):
        '''
        is_flashcard returns True if its the flashcard page

        :return: True if flashcard page
        :rtype: bool
        '''
        return self.input_data['category']['category_type'] == 'flashcard'

    def assign_category_div_variables(self, group, prefix):
        '''
        assign_category_div_variables assigns the div id for the group level divs

        for category pages, use the same data to link the side_menu group link to
        div that will show when the side menu is clicked

        for a flashcard page, use the group display div in a hidden variable that can track the next
        flashcard to display

        :param group: group information retrieved from the group db record
        :type group: dict
        :param prefix: A <br> to separaee side menu links or a tilde to separate the hidden group ids
        :type prefix: str
        :return: the group that now has the group_div_id to use in the template
        :rtype: dict
        '''
        link_text = group['group_identifier']
        group_div_id = link_text.replace(' ', '_').lower()
        group['group_div_id'] = group_div_id

        if self.is_flashcard():
            group['group_div_class'] = 'flashcard_group_div'
            self.hidden_flashcard_divs += prefix + group_div_id
        else:
            group['group_div_class'] = 'd-none' if prefix else 'category_group_div'
            self.assign_side_menu(prefix, link_text, group_div_id)
        return group

    def assign_side_menu(self, prefix, link_text, group_div_id):
        '''
        assign_side_menu is the side menu used to select which group of paragraphs to display for
        a given category

        :param prefix: depending on which category this is the divider between group identifiers
        :type prefix: str
        :param link_text: is the text that displays on the sidemenu
        :type link_text: str
        :param group_div_id: is the id for the div to show or hide
        :type group_div_id: str
        '''
        menu_id = group_div_id + '_menu'
        link = (f'<a href="#" id={menu_id} data-identifier={group_div_id} class="category_group">'
                f'{link_text}</a>')
        self.side_menu += prefix + link
