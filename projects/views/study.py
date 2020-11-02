''' Study View classes '''
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse
from projects.forms.paragraphs import ParagraphLookupForm
import helpers.no_import_common_class.paragraph_helpers as no_import_para_helper
import helpers.no_import_common_class.utilities as utils
import helpers.import_common_class.paragraph_helpers as import_para_helper


INITIAL_CLASSIFICATION = [('0', 'Choose Classification')]


class StudyParagraphView(TemplateView):
    '''
    StudyParagraphView View standalone paragraphs

    :param TemplateView: Basic view
    :type TemplateView: Template View Class
    :return: context which includes the standard paragraph display object
    :rtype: dict
    '''
    template_name = 'projects/paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        context = import_para_helper.paragraph_view_input(context)
        return context


class StudyLookupView(FormView):
    ''' StudyLookupView is a form to choose the content to view'''

    template_name = 'projects/study_lookup.html'
    form_class = ParagraphLookupForm

    def get(self, request, *args, **kwargs):
        form_data = request.GET.get("classification", "0")
        in_data = no_import_para_helper.extract_data_from_form(form_data)
        if in_data:
            arg_dictionary = StudyLookupView.which_args(in_data)
            return HttpResponseRedirect(reverse(arg_dictionary['identifier'],
                                                kwargs=arg_dictionary['kwargs']))
        return super().get(request, *args, **kwargs)

    @staticmethod
    def which_args(in_data):
        '''
        which_args allows categories from the study selection go to the flashcard page and groups to go
        to the standalone paragraph page

        :param in_data: dictionary with group_id as a key or category_id as a key
        :type in_data: dict
        :return: information necessary for correct url construction
        :rtype: dict
        '''
        if utils.key_in_dictionary(in_data, 'category'):
            identifier = 'projects:study_paragraphs_with_category'
            kwargs = {'category_id': in_data['category']}
        else:
            identifier = 'projects:study_paragraphs_with_group'
            kwargs = {'group_id': in_data['group']}
        return {'identifier': identifier, 'kwargs': kwargs}
