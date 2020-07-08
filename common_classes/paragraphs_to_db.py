'''Used in batch process to create db records from JSON data.  JSON data in same format can be used
   to display the paragraph without creating a db record'''
from django.db import IntegrityError
from projects.models.paragraphs import (Group, GroupParagraph, Paragraph,
                                        Reference)
import helpers.no_import_common_class.paragraph_helpers as para_helper

# Todo: validate input json data --- this is one validation
VALID_STANDALONE = ('yes', 'no', 'depend_on_para')


class ParagraphsToDatabase:
    '''
    ParagraphsToDatabase is a class to display paragraphs.

    This web app uses paragraph display for most informational pages. This class
    is the basic functionality.

    :param object: inherits from object
    :type object: Object object
    '''
    def __init__(self):
        self.title = ''
        self.title_note = ''
        # 'fake_para_id': 'para_id'
        self.fake_to_real_para_id = {}
        self.standalone = None
        self.group = None
        self.ordered = False
        self.current_order_num = 0

    def dictionary_to_db(self, input_data):
        '''
        dictionary_to_db drives the db create (or update) process

        :param input_data: JSON data formatted into dictionary
        :type input_data: dict
        '''
        self.assign_group_data(input_data)
        res = self.find_or_create_group()
       # Review: when it comes time to figure out error handling strategy
        if res != 'ok':
            print(f'group not saved: group input == {input_data["group"]}, result returned {res} ')
            exit(1)
        self.find_or_create_references(input_data)
        self.create_paragraphs(input_data)
        self.associate_paragraphs_with_references(input_data)

    def assign_group_data(self, input_data):
        group_dict = input_data['group']
        self.title = group_dict['title']
        self.title_note = group_dict['note']
        self.standalone = group_dict['standalone']

    # Review: when it comes time to figure out error handling strategy
    def find_or_create_group(self):
        '''
        find_or_create_group will look for a group using the title, which must be unique.  It it
        does not exist, it will be created

        :return: string that says ok or an error message (may change later)
        :rtype: [type]
        '''
        try:
            group, created = Group.objects.get_or_create(
                title=self.title,
                note=self.title_note,
            )
            group.save()
        except IntegrityError:
            print('Integrity error while creating group.')
            return 'Integrity error while creating group.'
        self.group = group
        return 'ok'

    def find_or_create_references(self, input_data):
        '''
        find_or_create_references will find based on link_text which must be unique.

        :param input_data: references contain link_text & url. Multiple paras can have same reference
        :type input_data: dict
        '''
        references = input_data['references']
        for ref in references:
            reference, created = Reference.objects.get_or_create(
                link_text=ref['link_text'],
                url=ref['url'],
            )
            reference.save()

    # Todo: add some validation, for example the decide_standalone only has three valid possiblities
    def create_paragraphs(self, input_data):
        '''
        create_paragraphs takes the input_data from the JSON file input (just like display JSON), but
        this time actually creates the database records

        :param input_data: dictionary from JSON file to dictionary transformation
        :type input_data: dict
        '''
        para_list = input_data['paragraphs']
        for para in para_list:
            if self.ordered:
                self.current_order_num += 1
            para['standalone'] = self.decide_standalone(para)
            paragraph = self.create_paragraph_record(para)
            self.fake_to_real_para_id[para['id']] = paragraph.id
            self.add_association_with_group(paragraph)

    # Note: three valid values: VALID_STANDALONE = ('yes', 'no', 'depend_on_para')
    def decide_standalone(self, para):
        '''
        Decide_standalone says whether to make the  standalone field in the paragraph record
        True or False.

        If all the paragraphs in a given JSON file are True or False, then the data in the
        group record is sufficient ('yes' is True and 'no' is False).

        BUT if the group record says 'depend_on_para' then that means that the JSON file is
        responsible to saying whether the paragraph stands alone.  (For flashcards, the questions
        will not standalone, but the answers probably will)

        The standalone field in the paragraph record will be used eliminate non-standalone paragraphs
        when doing a search string or tag search when there is no group or catagory chosen.  In that case, the
        rule is that only standalone records will be retrieved.  This field is in the paragraph
        because a given group can have some standalone and some not-standalone records

        :param para: paragraph record from the input
        :type para: dict
        :return: True or False based on whether the paragraph stands alone
        :rtype: Boolean
        '''
        if self.standalone == 'yes':
            return True
        elif self.standalone == 'no':
            return False
        if para['standalone'] == 'yes':
            return True
        return False

    def associate_paragraphs_with_references(self, input_data):
        '''
        associate_paragraphs_with_references creates the paragraph to reference association

        :param input_data: dictionary created from reading the JSON file used to create the paragraphs
        :type input_data: dict
        '''
        ref_link_paras = input_data['ref_link_paragraph']
        for ref_para in ref_link_paras:
            ref = Reference.objects.get(link_text=ref_para['link_text'])
            para = Paragraph.objects.get(pk=self.fake_to_real_para_id[ref_para['paragraph_id']])
            ref.paragraphs.add(para)

    def create_paragraph_record(self, para):
        '''
        create_paragraph_record creates paragraph records.  This does not do a uniqueness check!
        This calls format_json_text which takes the paragraph text as formatted in the JSON file and
        transforms it to a str as needed to store in atabase and use in ParagraphsForDisplay

        :param para: JSON file to dictionary format
        :type para: dict
        :return: paragraph record
        :rtype: db record
        '''
        paragraph = Paragraph.objects.create(
            subtitle=para['subtitle'],
            standalone=para['standalone'],

            note=para['note'],
            text=para_helper.format_json_text(para['text'])
        )
        paragraph.save()
        return paragraph

    def add_association_with_group(self, paragraph):
        '''
        add_association_with_group associates a paragraph with a group record

        :param paragraph: paragraph that was just created
        :type paragraph: db record
        '''
        group_para = GroupParagraph.objects.create(group=self.group, paragraph=paragraph,
                                                   order=self.current_order_num)
        group_para.save()
