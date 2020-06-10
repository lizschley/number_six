from django import forms


INFORMATION_TYPES = (
    ('', 'Choose Information Type'),
    ('1', 'First'),
    ('2', 'Second')
)


class ParagraphLookupForm(forms.Form):
    information_type = forms.ChoiceField(label='Information Type', choices=INFORMATION_TYPES)

