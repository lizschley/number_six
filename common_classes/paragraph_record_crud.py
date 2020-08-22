'''These will be static resusable methods to create &/or update records'''
from projects.models.paragraphs import (Category, Reference, Paragraph, Group, GroupParagraph,
                                        ParagraphReference)

# Todo: validate input json data --- this is one validation
VALID_STANDALONE = ('yes', 'no', 'depend_on_para')


class ParagraphRecordCrud:
    '''
    ParagraphsRecordCreateOrUpdate is a class of static methods to retrieve, update or create
    paragraph associated records.

    :param object: inherits from object
    :type object: Object object
    '''

    @staticmethod
    def find_or_create_category(category_in):
        '''
        find_or_create_category retrieve or create category

        :param category_data: data necessary to create a new category
        :type category_data: dict
        '''
        try:
            category = Category.objects.get(
                title=category_in['title']
            )
        except category.DoesNotExist:
            category = ParagraphRecordCrud.create_category(category_in)
        return category

    @staticmethod
    def create_category(category_in):
        '''
        create_category creates a category record

        :param category_in: [description]
        :type category_in: [type]
        :return: [description]
        :rtype: [type]
        '''

        category = Category(
            title=category_in['title'],
            category_type=category_in['type']
        )
        category.save()
        return category.objects.get(category_in['title'])

    @staticmethod
    def retrieve_category(category_in):
        '''
        retrieve_category retrieves a category or returns None if it does not exist

       :param category_data: data necessary to create a new category
        :type category_data: dict
        :return: category record or None
        :rtype: category
        '''
        try:
            category = Category.objects.get(
                title=category_in['title'],
                note=category_in['note']
            )
        except category.DoesNotExist:
            category = None
        return category




    @staticmethod
    def find_or_create_group(group_in):
        '''
        find_or_create_group retrieve or create groups

        :param group_data: data necessary to create a new group
        :type group_data: dict
        '''
        try:
            group = Group.objects.get(
                title=group_in['title']
            )
        except Group.DoesNotExist:
            group = ParagraphRecordCrud.create_group(group_in)
        return group

    @staticmethod
    def create_group(group_in):
        '''
        create_group creates a group record

        :param group_in: [description]
        :type group_in: [type]
        :return: [description]
        :rtype: [type]
        '''

        group = Group(
            title=group_in['title'],
            note=group_in['note']
        )
        group.save()
        return Group.objects.get(group_in['title'])

    @staticmethod
    def retrieve_group(group_in):
        '''
        retrieve_group retrieves a group or returns None if it does not exist

       :param group_data: data necessary to create a new group
        :type group_data: dict
        :return: Group record or None
        :rtype: Group
        '''
        try:
            group = Group.objects.get(
                title=group_in['title'],
                note=group_in['note']
            )
        except Group.DoesNotExist:
            group = None
        return group

#####################################################################################

    def find_or_create_references(self, input_data):
        '''
        find_or_create_references will find based on link_text which must be unique.

        :param input_data: references contain link_text & url. Multiple paras can have same reference
        :type input_data: dict
        '''
        references = input_data['references']
        for ref in references:
            try:
                reference = Reference.objects.get(
                                link_text=ref['link_text'],
                                url=ref['url']
                            )
            except Reference.DoesNotExist:
                reference = Reference(
                                link_text=ref['link_text'],
                                url=ref['url']
                            )
                reference.save()




###############################################



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
        if self.standalone == 'yes':
            return True
        if self.standalone == 'no':
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
            para.references.add(ref)

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
            image_path=para['image_path'],
            image_info_key=para['image_info_key'],
            text=para_helper.format_json_text(para['text'])
        )
        return paragraph

    def add_association_with_group(self, paragraph):
        '''
        add_association_with_group associates a paragraph with a group record

        :param paragraph: paragraph that was just created
        :type paragraph: db record
        '''
        GroupParagraph.objects.create(group=self.group, paragraph=paragraph,
                                      order=self.current_order_num)
