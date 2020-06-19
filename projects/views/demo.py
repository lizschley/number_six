from django.views.generic import TemplateView
import os
import portfolio.settings as ps
import helpers.scripts_or_views.non_class_helpers as nch

DEMO_PARAGRAPH_JSON = os.path.join(ps.JSON_DATA_ROOT, 'demo/urban_coyotes.json')


class DemoParagraphView(TemplateView):
    template_name = 'projects/paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        context['path_to_json'] = DEMO_PARAGRAPH_JSON
        context = nch.paragraph_view_input(context)
        return context
