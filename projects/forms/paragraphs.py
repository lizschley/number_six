''' Django Form '''
from django import forms
import helpers.no_import_common_class.lookup_form_helpers as from_db


CLASSIFICATION_CHOICES = from_db.get_initial_classifications()


class ParagraphLookupForm(forms.Form):
    ''' A way for users to choose what they want to see '''
    classification = forms.ChoiceField(label='Classification:',
                                       choices=CLASSIFICATION_CHOICES, required=False,)
