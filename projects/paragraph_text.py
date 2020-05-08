
from utilities.representations import AsDictionaryMixin


class ParagraphText(AsDictionaryMixin):
    def retrieve_output_text(self, group, paragraphs):
        self.group = group
        self.paragraphs = paragraph

    def __repr__(self):
        return print_dict(self.to_dict())

