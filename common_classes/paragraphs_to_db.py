from django.db import IntegrityError
from projects.models.paragraphs import Group
from projects.models.paragraphs import Paragraph
from projects.models.paragraphs import GroupParagraph
from projects.models.paragraphs import Reference
import utilities.paragraph_helpers as ph


VALID_STANDALONE = ('yes', 'no', 'depend_on_para')


class ParagraphsToDatabase(object):
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
        self.assign_group_data(input_data)
        res = self.find_or_create_group()
        if not res == 'ok':
            exit(1)
        self.find_or_create_references(input_data)
        self.create_paragraphs(input_data)
        self.associate_paragraphs_with_references(input_data)

    def assign_group_data(self, input_data):
        group_dict = input_data['group']
        self.title = group_dict['title']
        self.title_note = group_dict['note']
        self.standalone = group_dict['standalone']

    def find_or_create_group(self):
        try:
            group, created = Group.objects.get_or_create(
                title=self.title,
                note=self.title_note,
            )
            group.save()
        except IntegrityError as e:
            print(e.message)
            return e.message
        self.group = group
        return 'ok'

    def find_or_create_references(self, input_data):
        references = input_data['references']
        for ref in references:
            reference, created = Reference.objects.get_or_create(
                link_text=ref['link_text'],
                url=ref['url'],
            )
            reference.save()

    def create_paragraphs(self, input_data):
        para_list = input_data['paragraphs']
        for para in para_list:
            if self.ordered:
                self.current_order_num += 1
            para['standalone'] = self.decide_standalone(para)
            paragraph = self.create_paragraph_record(para)
            self.fake_to_real_para_id[para['id']] = paragraph.id
            self.add_association_with_group(paragraph)

    def decide_standalone(self, para):
        if self.standalone == 'yes':
            return True
        elif self.standalone == 'no':
            return False
        if para['standalone'] == 'yes':
            return True
        return False

    def associate_paragraphs_with_references(self, input_data):
        ref_link_paras = input_data['ref_link_paragraph']
        for ref_para in ref_link_paras:
            ref = Reference.objects.get(link_text=ref_para['link_text'])
            para = Paragraph.objects.get(pk=self.fake_to_real_para_id[ref_para['paragraph_id']])
            ref.paragraphs.add(para)

    def create_paragraph_record(self, para):
        paragraph = Paragraph.objects.create(
            subtitle=para['subtitle'],
            standalone=para['standalone'],
            note=para['note'],
            text=ph.format_json_text(para['text'])
        )
        paragraph.save()
        return paragraph

    def add_association_with_group(self, paragraph):
        group_para = GroupParagraph.objects.create(group=self.group, paragraph=paragraph,
                                                   order=self.current_order_num)
        group_para.save()
