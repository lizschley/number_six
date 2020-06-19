from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from projects.forms.paragraphs import ParagraphLookupForm
import helpers.scripts_or_views.non_class_helpers as nch
from django.urls import reverse


DEMO_PARAGRAPH_JSON = 'data/demo/urban_coyotes.json'
INITIAL_CLASSIFICATION = [('0', 'Choose Classification')]


class StudyParagraphView(TemplateView):
    template_name = 'projects/paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        context = nch.paragraph_view_input(context)
        return context


class StudyLookupView(FormView):
    template_name = 'projects/study_lookup.html'
    form_class = ParagraphLookupForm

    def get(self, request, *args, **kwargs):
        # TODO turn extract data from form into whatever makes this code the cleanest
        in_data = ph.extract_data_from_form(request.GET.get("classification", "0"))
        print(f'in study lookup get ---> in_data=={in_data}')
        if in_data:
            return HttpResponseRedirect(reverse('projects:study_paragraphs_with_group',
                                        kwargs={'group_id': in_data['group']}))
        else:
            return super().get(request, *args, **kwargs)
