'''Used in batch process to create db records from JSON data.  JSON data in same format can be used
   to display the paragraph without creating a db record'''
import sys
from common_classes.para_db_methods import ParaDbMethods
import helpers.no_import_common_class.utilities as utils
from projects.models.paragraphs import (Group, GroupParagraph, Paragraph, Reference)


class ParaDbCreateProcess(ParaDbMethods):
    '''
    ParaDbCreateProcess is a class to display paragraphs.

    This web app uses paragraph display for most informational pages. This class
    is the basic functionality.

    :param object: inherits from object
    :type object: Object object
    '''
    def __init__(self, updating=False):
        super(ParaDbCreateProcess, self).__init__(updating)
        self.title = ''
        # 'fake_para_id': 'para_id'
        self.fake_to_real_para_id = {}
        self.standalone = None
        self.group = None
        self.ordered = False
        self.current_order_num = 0
        self.input_data = {}

    def dictionary_to_db(self, input_data):
        '''
        dictionary_to_db drives the db create (or update) process

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
        process_group will look for a group using the title, which must be unique.  It it
        does not exist, it will be created

        :return: string that says ok or an error message (may change later)
        :rtype: [type]
        '''
        self.assign_group_data()
        find_dict = {'title': self.title}
        creating = self.expect_to_create_group()
        if not creating:
            return_data = {}
            return_data['record'] = self.find_record(Group, find_dict)
        else:
            create_dict = {'title': self.title,
                           'note': self.input_data['group']['group_note'],
                           'category_id': self.input_data['group']['category_id'],
                           'short_name': self.input_data['group']['short_name'],
                           'group_type': self.input_data['group']['group_type'],
                           'cat_sort': self.cat_sort(), }
            return_data = self.find_or_create_record(Group, find_dict, create_dict)
        if self.updating:
            self.group = return_data['record']

    def expect_to_create_group(self):
        '''
        expect_to_create_group returns True if the user wants to create a new group

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
        self.standalone = group_dict['standalone']
        if group_dict['ordered'] == 'yes':
            self.ordered = True

    def cat_sort(self):
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

    # Todo: add some validation, for example the decide_standalone only has three valid possiblities
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
            if utils.key_in_dictionary(para, 'link_text_list'):
                self.add_ref_para_association(para)
                para.pop('link_text_list')
            paragraph = self.create_paragraph_record(para)
            self.fake_to_real_para_id[para['id']] = paragraph.id
            self.add_association_with_group(paragraph)

    def add_ref_para_association(self, para):
        '''
        add_ref_para_association is a convenience method allowing the user to simply list the link text
        associated with given para, instead of having manually associating each link to its paragraphs

        :param para: one paragraph record
        :type para: dict
        '''
        if not para['link_text_list']:
            return
        if utils.key_not_in_dictionary(self.input_data, 'ref_link_paragraph'):
            self.input_data['ref_link_paragraph'] = []
        ref_para_association = utils.add_to_associations('paragraph_id',
                                                         para['id'],
                                                         'link_text',
                                                         para['link_text_list'],
                                                         self.input_data['ref_link_paragraph'])
        self.input_data['ref_link_paragraph'] = ref_para_association

    def decide_standalone(self, para):
        '''
        Decide_standalone says whether to make the  standalone field in the paragraph record
        True or False.
        If all the paragraphs in a given JSON file are True or False, then the data in the
        group record is sufficient ('yes' is True and 'no' is False).
        BUT if the group record says 'depend_on_para' then that means that the JSON file is
        responsible to saying whether the paragraph stands alone.  (For flashcards, the questions
        will not standalone, but the answers probably will)
        The standalone field in the paragraph record will be used eliminate non-standalone
        paragraphs when doing a search string or tag search when no group or catagory is chosen.
        In that case, the rule is that only standalone records will be retrieved.  This field
        is in the paragraph because a given group can have some standalone and
        some not-standalone records
        :param para: paragraph record from the input
        :type para: dict
        :return: True or False based on whether the paragraph stands alone
        :rtype: Boolean
        '''
        standalone = para.get('standalone', 'default')
        if standalone == 'default':
            standalone = self.standalone
        if utils.key_in_dictionary(para, 'standalone'):
            return
        if standalone == 'yes':
            return True
        if standalone == 'no':
            return False
        return False

    def associate_paragraphs_with_references(self):
        '''
        associate_paragraphs_with_references creates the paragraph to reference association
        '''
        if utils.key_not_in_dictionary(self.input_data, 'ref_link_paragraph'):
            return
        ref_link_paras = self.input_data['ref_link_paragraph']
        for ref_para in ref_link_paras:
            ref = Reference.objects.get(link_text=ref_para['link_text'])
            para = Paragraph.objects.get(pk=self.fake_to_real_para_id[ref_para['paragraph_id']])
            para.references.add(ref)

    # Todo: Remove the fake ids in this process, but that is for later cleanup
    def create_paragraph_record(self, para):
        '''
        create_paragraph_record creates paragraph records.  This does not do a uniqueness check!
        We need the fake id to associate with records, so we do a shallow copy in order to remove
        the id key from the dictionary we will use to create the record.
        :param para: JSON file to dictionary format
        :type para: dict
        :return: paragraph record
        :rtype: db record
        '''
        create_dict = para.copy()
        del create_dict['id']
        create_dict['text'] = para['text']
        return self.create_record(Paragraph, create_dict)

    def add_association_with_group(self, paragraph):
        '''
        add_association_with_group associates a paragraph with a group record
        :param paragraph: paragraph that was just created
        :type paragraph: db record
        '''
        create_dict = {'group_id': self.group.id, 'paragraph_id': paragraph.id,
                       'order': self.current_order_num}
        return self.create_record(GroupParagraph, create_dict)
