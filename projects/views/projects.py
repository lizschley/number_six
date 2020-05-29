from django.shortcuts import get_object_or_404
from django.shortcuts import render
from projects.models.projects import Project
from django.views.generic import TemplateView


# Create your views here.
def all_projects(request):
    projects = Project.objects.all().order_by('id')
    return render(request, 'projects/all_projects.html', {'projects': projects})


class ProjectDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        slug = context['slug']
        context = {
            'project': get_object_or_404(Project, slug=slug)  # pass slug
        }
        print(f'context={context}')
        if slug == 'demo':
            self.template_name = 'projects/demo.html'
        elif slug == 'exercise':
            self.template_name = 'projects/exercise.html'
        else:
            self.template_name = 'projects/study.html'
        return context


class ProjectDemoView(TemplateView):
    template_name = 'projects/demo.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        return context


class ProjectStudyView(TemplateView):
    template_name = 'projects/study.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        return context


class ProjectExerciseView(TemplateView):
    template_name = 'projects/exercise.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        return context
