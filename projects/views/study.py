from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from projects.forms.paragraphs import ParagraphLookupForm
import helpers.paragraph_helpers as ph


DEMO_PARAGRAPH_JSON = 'data/demo/urban_coyotes.json'
INITIAL_CLASSIFICATION = [('0', 'Choose Classification')]


class StudyParagraphView(TemplateView):
    template_name = 'projects/paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        paragraphs = ph.paragraph_list_from_json(DEMO_PARAGRAPH_JSON)
        context = ph.context_for_paragraphs(context, paragraphs)
        return context


class StudyLookupView(FormView):
    template_name = 'projects/study_lookup.html'
    form_class = ParagraphLookupForm
    success_url = 'projects/study/paragraphs'

    def get(self, request, *args, **kwargs):
        print(f'request params == {request.GET.get("classification", "0")}')
        input = ph.extract_ids_from_classification(request.GET.get("classification", "0"))
        print(f'input=={input}')
        return super().get(request, *args, **kwargs)

