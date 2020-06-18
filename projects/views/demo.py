from django.views.generic import TemplateView
import helpers.paragraph_helpers as ph
import os
import portfolio.settings as ps

DEMO_PARAGRAPH_JSON = os.path.join(ps.JSON_DATA_ROOT, 'demo/urban_coyotes.json')


class DemoParagraphView(TemplateView):
    template_name = 'projects/paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        print(f'context=={context}')
        paragraphs = ph.paragraph_list_from_json(DEMO_PARAGRAPH_JSON)
        context = ph.context_for_paragraphs(context, paragraphs)
        return context
