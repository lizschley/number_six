''' Study View classes '''
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse
from projects.forms.paragraphs import ParagraphLookupForm
import helpers.no_import_common_class.paragraph_helpers as no_import_para_helper
import helpers.import_common_class.paragraph_helpers as import_para_helper


INITIAL_CLASSIFICATION = [('0', 'Choose Classification')]


class StudyParagraphView(TemplateView):
    template_name = 'projects/paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        context = import_para_helper.paragraph_view_input(context)
        return context


class StudyLookupView(FormView):
    template_name = 'projects/study_lookup.html'
    form_class = ParagraphLookupForm

    def get(self, request, *args, **kwargs):
        # Todo: turn extract data from form into whatever makes this code the cleanest
        form_data = request.GET.get("classification", "0")
        in_data = no_import_para_helper.extract_data_from_form(form_data)
        if in_data:
            return HttpResponseRedirect(reverse('projects:study_paragraphs_with_group',
                                        kwargs={'group_id': in_data['group']}))
        else:
            return super().get(request, *args, **kwargs)
