''' Django Form '''
from django import forms
import helpers.no_import_common_class.lookup_form_helpers as from_db


CHOICES = from_db.study_dropdowns()


class ParagraphLookupForm(forms.Form):
    ''' A way for users to choose what they want to see '''
    ordered = forms.ChoiceField(label='Ordered Paragraphs:',
                                choices=CHOICES['ordered'], required=False,)
    standalone = forms.ChoiceField(label='Standalone Paragraphs:',
                                   choices=CHOICES['standalone'], required=False,)
    flashcard = forms.ChoiceField(label='Flashcards:',
                                  choices=CHOICES['flashcard'], required=False,)
    search = forms.ChoiceField(label='Search:',
                               widget=forms.TextInput(attrs={'placeholder': '> 2 characters'}),
                               required=False,)
