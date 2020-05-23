from django.views.generic import TemplateView


class DemoScreenScrapingView(TemplateView):
    template_name = 'projects/demo/demo_paragraphs.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        return context
