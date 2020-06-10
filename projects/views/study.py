from django.views.generic import TemplateView
from django.views.generic.edit import FormView
import utilities.paragraph_helpers as ph
from projects.forms.paragraphs import ParagraphLookupForm

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


class StudyLookupView(FormView):
    template_name = 'projects/study_lookup.html'
    form_class = ParagraphLookupForm
    success_url = 'study/paragraphs'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)
