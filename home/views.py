''' Home based pages: home, resume and blog (future implementation) '''
from django.shortcuts import render
from django.views.generic import TemplateView
import helpers.import_common_class.paragraph_helpers as para_helper
from common_classes.paragraphs_for_display_cat import ParagraphsForDisplayCat


def home(request):
    return render(request, 'home/home.html')


class ResumeView(TemplateView):
    ''' This will be a basic category page (like the exercise page or blogs) '''
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        self.template_name = 'category.html'
        context = self._add_to_context(context)
        return context

    def _add_to_context(self, context):
        context['slug'] = 'resume'
        context = para_helper.paragraph_view_input(context, False, ParagraphsForDisplayCat)
        return context
