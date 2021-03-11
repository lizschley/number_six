'''Used in batch process to create db records from JSON data.  JSON data in same format can be used
   to display the paragraph without creating a db record'''
import sys
from common_classes.para_db_methods import ParaDbMethods
import constants.crud as crud
import helpers.no_import_common_class.paragraph_helpers as helpers
import utilities.random_methods as utils
from projects.models.paragraphs import (Group, GroupParagraph, Paragraph, Reference)


class ParaDbCreateProcess(ParaDbMethods):
    '''
        ParaDbCreateProcess is the only class to create paragraphs.  It also has the ability to create
        groups, references and the the GroupParagraph and ParagraphReference associations.

        ParaDbCreateProcess does not create categories (because there are not many different categories,
        and because they have no direct association with Paragraphs).  Groups and references, and their
        associations, can also be created in the update process.

        :param object: inherits from ParaDbMethods
        :type object: ParaDbCreateProcess
    '''
    def __init__(self, updating=False):
        super().__init__(updating)
        self.title = ''
        self.fake_to_real_para_id = {}
        self.group = None
        self.ordered = False
        self.current_order_num = 0
        self.input_data = {}

    def dictionary_to_db(self, input_data):
        '''
            dictionary_to_db drives the db create process

            :param input_data: JSON data formatted into dictionary
            :type input_data: dict
        '''
        self.input_data = input_data
        self.process_group()
        self.find_or_create_references()
        if not self.updating:
            sys.exit(1)
        self.create_paragraphs()
        self.associate_paragraphs_with_references()

    def process_group(self):
        '''
            process_group will look for a group using the title, which must be unique.  If it
            does not exist, it will be created

            :return: string that says ok or an error message (may change later)
            :rtype: [type]
        '''
        self.assign_group_data()
        find_dict = {'title': self.title}
        creating = self.expect_to_create_group()
        if not creating:
            return_data = {'record': self.find_record(Group, find_dict)}
        else:
            create_dict = {'title': self.title,
                           'note': self.input_data['group']['group_note'],
                           'category_id': self.input_data['group']['category_id'],
                           'short_name': self.input_data['group']['short_name'],
                           'group_type': self.input_data['group']['group_type'],
                           'cat_sort': self.cat_sort(), }
            return_data = self.find_or_create_record(Group, find_dict, create_dict)
        if self.updating:
            self.ordered = not return_data['record'].group_type in ('standalone', 'no_search', 'search')
            self.group = return_data['record']
        else:
            self.ordered = False

    def expect_to_create_group(self):
        '''
            expect_to_create_group returns True if the user wants to create a new group

            Its purpose is to fail early if a group for a given title does not exist, in order
            to prevent a title change or typo making it so garbage groups and group para relationships
            are created

            :return: returns True if the user wants to create a new group
            :rtype: bool
        '''
        if utils.key_not_in_dictionary(self.input_data['group'], 'short_name'):
            return False
        if len(self.input_data['group']['short_name']) > 2:
            return True
        return False

    def assign_group_data(self):
        '''
            assign_group_data to instance variables
        '''
        group_dict = self.input_data['group']
        self.title = group_dict['group_title']

    def cat_sort(self):
        '''
            cat_sort returns a new cat_sort for the group that is being created

            :return: cat_sort that is one higher than the largest cat_sort within a category
            :rtype: int
        '''
        if not self.input_data['group']['category_id']:
            return None
        return self.max_cat_sort_for_given_category(self.input_data['group']['category_id'])

    def find_or_create_references(self):
        '''
            find_or_create_references will find based on link_text which must be unique.
        '''
        if utils.key_not_in_dictionary(self.input_data, 'references'):
            return
        references = self.input_data['references']
        for ref in references:
            create_dict = {'link_text': ref['link_text'], 'url': ref['url'],
                           'short_text': ref['short_text']}
            find_dict = {'link_text': ref['link_text']}
            ref = self.find_or_create_record(Reference, find_dict, create_dict)

    def create_paragraphs(self):
        '''
            create_paragraphs takes the input_data from the JSON file input (just like display JSON), but
            this time actually creates the database records
        '''
        para_list = self.input_data['paragraphs']
        for para in para_list:
            if self.ordered:
                self.current_order_num += 1
            para['standalone'] = self.decide_standalone(para)
            self.link_text_list(para)
            self.add_short_title(para['standalone'], para)
            paragraph = self.create_paragraph_record(para)
            self.fake_to_real_para_id[para['id']] = paragraph.id
            self.add_association_with_group(paragraph)

    def add_short_title(self, standalone, para):
        '''
            add_short_title is a convenience method so that the subtitle will be used for modal popups
            and internal links to standalone paragraphs unless it is too long

            :param standalone: if the paragraph can be independant from other paragraphs in the group
            :type standalone: bool
            :param para: a unit of text that had lots of associated information
            :type para: dict
        '''
        if not standalone:
            return
        if len(para['subtitle']) > 50:
            return
        if not utils.valid_non_blank_string(para['short_title']):
            para['short_title'] = para['subtitle']

    def link_text_list(self, para):
        '''
            link_text_list initiates the process of turning the list of references' link_text to
            associations between a given paragraph and all of its references

            :param para: one paragraph
            :type para: dict
        '''
        if utils.key_not_in_dictionary(self.input_data, 'ref_link_paragraph'):
            self.input_data['ref_link_paragraph'] = []

        updated_para_ref = helpers.initiate_paragraph_associations(para,
                                                                   crud.PARA_ID_REF_LINK_TEXT,
                                                                   self.input_data['ref_link_paragraph'])
        if updated_para_ref is not None:
            self.input_data['ref_link_paragraph'] = updated_para_ref
        if utils.key_in_dictionary(para, 'link_text_list'):
            para.pop('link_text_list')

    def decide_standalone(self, para):
        '''
            Decide_standalone says whether to make the standalone field in the paragraph record
            True or False.  If self.ordered is False (group_type is standalone), the paragraph must be a
            standalone paragraph, even if it is used elsewhere as part of an ordered group.

            If the group is ordered, but the paragraph is designed to also be a standalone paragraph then
            the paragraph record will be standalone. In this case, it is up to the person creating the
            input data to make sure the paragraph is standalone.

            :param para: paragraph record from the input
            :type para: dict
            :return: True or False based on whether the paragraph stands alone
            :rtype: Boolean
        '''
        if not self.ordered:
            return True
        if utils.key_not_in_dictionary(para, 'standalone'):
            return False
        return True if para['standalone'] in ('yes', 'true', 'True') else False

    def associate_paragraphs_with_references(self):
        '''
            associate_paragraphs_with_references deals with the association table for paragraphs to
            references. It was a pain to create manually, so now it is created programmatically
            (see self.link_text_list()).  The association is made, as part of the create paragraph
            process with 'link_text_list': []. OR as part of the update paragraph process
            (ParaDbUpdateProcess) with either 'ref_slug_list': [] or 'link_text_list': [].

            All variations link through the list of unique reference fields and associate the reference
            with the paragraph that was just created or updated (in another class).  This is easier in
            terms of creating the data.

            Note - the para reference association is made after the paragraph, so there is no need
                   for a fake paragraph id.  It adds flexibility, however, so leaving for now
        '''
        if utils.key_not_in_dictionary(self.input_data, 'ref_link_paragraph'):
            return
        ref_link_paras = self.input_data['ref_link_paragraph']
        for ref_para in ref_link_paras:
            ref = Reference.objects.get(link_text=ref_para['link_text'])
            para = Paragraph.objects.get(pk=self.fake_to_real_para_id[ref_para['paragraph_id']])
            para.references.add(ref)

    def create_paragraph_record(self, para):
        '''
            create_paragraph_record creates paragraph records.  It does not do a uniqueness check!

            :param para: JSON file to dictionary format
            :type para: dict
            :return: paragraph record
            :rtype: db record
        '''
        create_dict = self.assign_paragraph(para)
        return self.create_record(Paragraph, create_dict)

    def add_association_with_group(self, paragraph):
        '''
            add_association_with_group associates a paragraph with a group record
            :param paragraph: paragraph that was just created
            :type paragraph: db record
        '''
        create_dict = {'group_id': self.group.id,
                       'paragraph_id': paragraph.id,
                       'order': self.current_order_num}
        return self.create_record(GroupParagraph, create_dict)

    def assign_paragraph(self, para):
        ''' returns new paragraph dictionary to use for creation '''
        return {
            'subtitle': para['subtitle'],
            'note': para['note'],
            'text': para['text'],
            'standalone': para['standalone'],
            'image_path': para['image_path'],
            'image_info_key': para['image_info_key'],
            'short_title': para['short_title'],
        }
