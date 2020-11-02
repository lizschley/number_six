''' Study View classes '''
from django.views.generic import TemplateView
import helpers.import_common_class.paragraph_helpers as import_para_helper
from common_classes.paragraphs_for_display_cat import ParagraphsForDisplayCat


class FlashCardView(TemplateView):
    template_name = 'projects/flash_card.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        context = import_para_helper.paragraph_view_input(context, False, ParagraphsForDisplayCat)
        return context
