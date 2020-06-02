from django.views.generic import TemplateView
import utilities.paragraph_helpers as ph

DEMO_PARAGRAPH_JSON = 'data/demo/urban_coyotes.json'


class StudyParagraphView(TemplateView):
    template_name = 'projects/paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        paragraphs = ph.paragraph_list_from_json(DEMO_PARAGRAPH_JSON)
        context = ph.context_for_paragraphs(context, paragraphs)
        return context
