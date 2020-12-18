'''This view displays the paragraphs in a basic fashion.'''
from django.http import JsonResponse
from django.views.generic import TemplateView
import constants.file_paths as file_paths
import helpers.import_common_class.paragraph_helpers as import_para_helper


class DemoParagraphView(TemplateView):
    ''' This is called from the project detail page.  It gives information about the site. '''
    template_name = 'projects/single_or_ordered_paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        # print(f'from view: {context}')
        return context

    def _add_to_context(self, context):
        context['path_to_json'] = file_paths.DEMO_PARAGRAPH_JSON
        context = import_para_helper.paragraph_view_input(context, True)
        return context


def para_by_subtitle(request):
    '''
    para_by_subtitle retrieves one paragraph and displays in a modal

    :param request: request object
    :type request: request
    :return: JSON (serialized) version of a dictionary with a single paragraph display object
    :rtype: JSON
    '''
    if request.method == 'GET' and request.is_ajax():
        subtitle = request.GET.get('subtitle')
    else:
        return JsonResponse({'success': False}, status=400)
    para = import_para_helper.single_para_by_subtitle(subtitle)
    return JsonResponse({'paragraph': para}, status=200)
