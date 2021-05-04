''' Study View classes '''
from django.views.generic import TemplateView
import helpers.import_common_class.paragraph_helpers as import_para_helper
from common_classes.paragraphs_for_display import ParagraphsForDisplay


class SearchParagraphsView(TemplateView):
    '''
    SearchParagraphsView displays paragraphs that are built programmatically for the search results

    :param TemplateView: Basic view
    :type TemplateView: Template View Class
    :return: context which includes the standard paragraph display object
    :rtype: dict
    '''

    template_name = 'projects/single_or_ordered_paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        context = import_para_helper.paragraph_view_input(context)
        return context
