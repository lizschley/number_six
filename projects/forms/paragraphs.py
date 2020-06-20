from django import forms
import helpers.no_import_common_class.lookup_form_helpers as from_db


CLASSIFICATION_CHOICES = from_db.get_initial_classifications()


class ParagraphLookupForm(forms.Form):
    classification = forms.ChoiceField(label='Classification:', choices=CLASSIFICATION_CHOICES, required = False,)
