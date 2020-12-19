''' Study View classes '''
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse
from projects.forms.paragraphs import ParagraphLookupForm
import helpers.no_import_common_class.lookup_form_helpers as lookup
import helpers.no_import_common_class.utilities as utils
import helpers.import_common_class.paragraph_helpers as import_para_helper


STANDALONE_TMPLT = 'projects/paragraphs.html'
ORDERED_TMPLT = 'projects/single_or_ordered_paragraphs.html'


class StudyParagraphView(TemplateView):
    '''
    StudyParagraphView View standalone paragraphs

    :param TemplateView: Basic view
    :type TemplateView: Template View Class
    :return: context which includes the standard paragraph display object
    :rtype: dict
    '''

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        if utils.key_not_in_dictionary(context, 'ordered'):
            self.template_name = STANDALONE_TMPLT
            return context
        self.template_name = ORDERED_TMPLT if context['ordered'] else STANDALONE_TMPLT
        return context

    def _add_to_context(self, context):
        context = import_para_helper.paragraph_view_input(context)
        return context


class StudyLookupView(FormView):
    ''' StudyLookupView is a form to choose the content to view'''

    template_name = 'projects/study_lookup.html'
    form_class = ParagraphLookupForm

    def get(self, request, *args, **kwargs):
        '''
        get processes the get parameters

        :param request: Request object containing the selected items from form
        :type request: WSGIRequest
        :return: Return data from form
        :rtype: dict
        '''
        input_from_form = {}
        input_from_form['ordered'] = request.GET.getlist('ordered')
        input_from_form['standalone'] = request.GET.getlist('standalone')
        input_from_form['flashcard'] = request.GET.getlist('flashcard')
        in_data = lookup.extract_data_from_form(input_from_form)
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


class OneParagraphView(TemplateView):
    '''
    OneParagraphView View standalone paragraphs on a single page (identified by slug)

    :param TemplateView: Basic view
    :type TemplateView: Template View Class
    :return: context which includes the standard paragraph display object
    :rtype: dict
    '''

    template_name = 'projects/single_or_ordered_paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        context = import_para_helper.single_para(context)
        return context


def para_by_subtitle(request):
    '''
    para_by_subtitle retrieves one paragraph and displays in a modal

    :param request: request object
    :type request: request
    :return: JSON (serialized) version of a dictionary with a single paragraph display object
    :rtype: JSON
    '''
    context = {}
    if request.method == 'GET' and request.is_ajax():
        context['subtitle'] = request.GET.get('subtitle')
    else:
        return JsonResponse({'success': False}, status=400)
    para = import_para_helper.single_para(context)
    return JsonResponse({'paragraph': para}, status=200)
