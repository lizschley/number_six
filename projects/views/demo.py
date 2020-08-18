'''This view displays the paragraphs in a basic fashion.'''
import os
from django.http import JsonResponse
from django.views.generic import TemplateView
import constants.file_paths as file_paths
import portfolio.settings as settings
import helpers.import_common_class.paragraph_helpers as import_para_helper


class DemoParagraphView(TemplateView):
    template_name = 'projects/demo_paragraphs.html'

    def get_context_data(self, **kwargs):
        context = self._add_to_context(super().get_context_data(**kwargs))
        # print(f'from view: {context}')
        return context

    def _add_to_context(self, context):
        context['path_to_json'] = file_paths.DEMO_PARAGRAPH_JSON
        context = import_para_helper.paragraph_view_input(context, True)
        return context


def para_by_subtitle(request):
    if request.method == 'GET' and request.is_ajax():
        subtitle = request.GET.get('subtitle')
    else:
        return JsonResponse({'success': False}, status=400)
    para = import_para_helper.single_para_by_subtitle(subtitle)
    return JsonResponse({'paragraph': para}, status=200)
