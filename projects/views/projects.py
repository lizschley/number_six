''' Original tutorial code.  Only Exercise uses the paragraphs functionality '''
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import TemplateView
import helpers.import_common_class.paragraph_helpers as para_helper
from common_classes.paragraphs_for_display_cat import ParagraphsForDisplayCat
from projects.models.projects import Project


# Create your views here.
def all_projects(request):
    ''' from original tuturial.  Show the original projects '''
    projects = Project.objects.all().order_by('id')
    return render(request, 'projects/all_projects.html', {'projects': projects})


class ProjectDetailView(TemplateView):
    ''' From original tutorial.  Pulled in paragraphs by Category for Exercise
        Demo and Study really just display informatin from the projects and text from the page. '''
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        if context['slug'] in ('exercise', 'amanda'):
            self.template_name = 'category.html'
            context = self._add_to_cat_context(context)
            return context
        slug = context['slug']
        context = {
            'project': get_object_or_404(Project, slug=slug)  # pass slug
        }
        if slug == 'demo':
            self.template_name = 'projects/demo.html'
        else:
            self.template_name = 'projects/study.html'
        return context

    def _add_to_cat_context(self, context):
        context['slug'] = 'at-home-exercise' if context['slug'] == 'exercise' else 'amanda-projects'
        context = para_helper.paragraph_view_input(context, False, ParagraphsForDisplayCat)
        return context
