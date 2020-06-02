from django.urls import path
from projects.views.projects import ProjectDetailView
from projects.views.demo import DemoParagraphView
from projects.views import projects

app_name = 'projects'

urlpatterns = [
    path('', projects.all_projects, name='all_projects'),
    path('<slug:slug>', ProjectDetailView.as_view(), name='detail'),
    path('demo', ProjectDetailView.as_view(), name='demo_landing_page'),
    path('study', ProjectDetailView.as_view(), name='study_landing_page'),
    path('exercise', ProjectDetailView.as_view(), name='exercise_landing_page'),
    path('demo/paragraphs', DemoParagraphView.as_view(), name='demo_paragraphs'),
    path('study/paragraphs', DemoParagraphView.as_view(), name='study_paragraphs'),
]
