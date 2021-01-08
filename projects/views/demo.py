''' demo view '''
from django.views.generic import TemplateView
import constants.file_paths as file_paths
import helpers.import_common_class.paragraph_helpers as import_para_helper


class DemoParagraphView(TemplateView):
    ''' This is called from the project detail page.  It gives information about the site. '''
    template_name = 'projects/single_or_ordered_paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        # print(f'from view: {context}')
        return context

    def _add_to_context(self, context):
        context['path_to_json'] = file_paths.DEMO_PARAGRAPH_JSON
        context = import_para_helper.paragraph_view_input(context, True)
        return context
