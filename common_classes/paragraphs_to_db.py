from django.db import IntegrityError
from projects.models.paragraphs import Group
from projects.models.paragraphs import Paragraph
from projects.models.paragraphs import GroupParagraph
from projects.models.paragraphs import Reference


VALID_STAND_ALONE = ('yes', 'no', 'depend_on_para')


class ParagraphsToDatabase(object):
    def __init__(self):
        self.title = ''
        self.title_note = ''
        # 'link_text': 'ref_id'
        self.reference_links = {}
        # 'fake_para_id': 'para_id'
        self.fake_to_real_para_id = {}
        self.para_id_to_reference = {}
        self.stand_alone = 'yes'
        self.group = None
        self.ordered = False

    def dictionary_to_db(self, input_data):
        self.assign_group_data(input_data)
        self.find_or_create_group()
        # self.find_or_create_references(input_data)
        self.create_paragraphs(input_data)
        self.associate_data(input_data)

    def assign_group_data(self, input_data):
        group_dict = input_data['group']
        self.title = group_dict['title']
        self.title_note = group_dict['note']
        self.stand_alone = group_dict['stand_alone']

    def find_or_create_group(self):
        try:
            group, created = Group.objects.get_or_create(
                title=self.title,
                note=self.title_note,
            )
            group.save()
        except IntegrityError as e:
            return print(e.message)
        print(f'group title {group.title}')
        print(f'group id {group.id}')
        print(group)
        self.group = group

    def find_or_create_references(self, input_data):
        references = input_data['references']
        for ref in references:
            self.reference_links[ref['link_text']] = ref['url']
            reference, created = Reference.objects.get_or_create(
                link_text=ref['link_text'],
                url=ref['url'],
            )
            reference.save()

    def create_paragraphs(self, input_data):
        pass
        # para_list = input_data['paragraphs']
        # self.paragraphs = []
        # for para in para_list:
        #     para['text'] = ph.format_json_text(para['text'])
        #     self.paragraphs.append(self.paragraph(para))
        #     self.add_links_to_paragraphs(input_data)

    def associate_data(self, input_data):
        self.associate_refs_to_para(input_data)
        self.associate_group_to_para(input_data)

    def associate_refs_to_para(self, input_data):
        pass
        # ref_para = input_data['ref_link_paragraph']
        # for para in self.paragraphs:
        #     associations = list(filter(lambda ref_par: para['id'] == ref_par['paragraph_id'], ref_para))
        #     para['references'] = self.paragraph_links_from_associations(associations)

    def associate_group_to_para(self, input_data):
        pass

    def paragraph(self, para):
        stand_alone = para['stand_alone'] if self.stand_alone == 'depend_on_para' else self.stand_alone
        para = {
            'subtitle': para['subtitle'],
            'subtitle_note': para['note'],
            'text': para['text'],
            'stand_alone': stand_alone,
        }
        return para
