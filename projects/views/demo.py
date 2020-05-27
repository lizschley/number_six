from django.views.generic import TemplateView
import utilities.paragraph_helpers as ph

DEMO_PARAGRAPH_JSON = 'data/demo/urban_coyotes.json'


class DemoParagraphView(TemplateView):
    template_name = 'projects/paragraphs.html'

    def get_context_data(self, **kwargs):
        # Here we will need the path (need to add this to the call
        # possible kwargs: group_id, search_tags, json_path
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        paragraphs = ph.paragraph_list_from_json(DEMO_PARAGRAPH_JSON)
        context['title'] = paragraphs['title']
        context['title_note'] = paragraphs['title_note']
        context['paragraphs'] = paragraphs['paragraphs']
        return context
