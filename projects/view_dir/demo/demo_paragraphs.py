from django.views.generic import TemplateView


class ProjectDemoParagraphView(TemplateView):
    template_name = 'projects/paragraphs.html'

    def get_context_data(self, **kwargs):
        # Here we will need the path (need to add this to the call
        # possible kwargs: group_id, search_tags, json_path
        context = self._add_to_context(super().get_context_data(**kwargs))
        return context

    def _add_to_context(self, context):
        context['json_filepath'] = 'data/demo/urban_coyotes.json'
        print(f'In view context=={context}')
        return context
