''' This class outputs a dictionary in a format used to display paragraphs.  It can be used
    for any page that either has only one group or that does not display by group.'''
import helpers.no_import_common_class.paragraph_helpers as para_helpers
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

    def format_data_for_display(self):
        '''
        format_data_for_display Once we know what class to use for retrieving the input data
        this is the main driver for the formatting process

        :return: dictionary to be added to the context & used in the paragraph display template
        :rtype: dict
        '''
        self.assign_title()
        self.create_links_from_references()
        self.assign_groups()
        return self.output_for_display()

    def assign_title(self):
        '''
        assign_title, for example title; paragraph displayer has no concept of group
        '''
        category = self.input_data['category']
        self.title = category['title'].strip()

    def assign_groups(self):
        '''
        assign_groups takes each group input, as retrieved in the the category retriever and
        makes it work for the category display
        '''
        for data in self.input_data['groups']:
            group = data['group']
            paragraphs = self.assign_paragraph_list(data['paragraphs'])
            ref_links = self.assign_ref_links(data['link_text'])
            self.groups.append(self.output_group(group, paragraphs, ref_links))

    def assign_paragraph_list(self, in_para_list):
        ''' assign_paragraphs - append the paragraph values needed with the keys that are expected '''
        out_para_list = []
        for para in in_para_list:
            para['text'] = para_helpers.replace_ajax_link_indicators(para['text'], False)
            para = para_helpers.add_image_information(para)
            out_para_list.append(self.paragraph(para))
        return out_para_list

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
        return {
            'group': group,
            'paragraphs': paragraphs,
            'ref_links': ref_links, }

    def output_for_display(self):
        '''
        output_for_display creates the **kwargs for the display paragraph template

        :return: final dict transformed in the study view to use in display paragraph template
        :rtype: dict
        '''
        return {'title': self.title,
                'groups': self.groups, }
