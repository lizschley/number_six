from django.shortcuts import render
from projects.models import Project


# Create your views here.
def all_projects(request):
    projects = Project.objects.all().order_by('id')
    print(request)
    return render(request, 'projects/all_projects.html', {'projects': projects})


def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    return render(request, 'projects/detail.html', {'project': project})


# is there a reason for having this?
# it may be leftover garbage
# Todo When everything is working, push and then delete below view and test everything again
def home(request):
    return render(request, 'projects/home.html')