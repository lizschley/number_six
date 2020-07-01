from django.urls import path
from projects.views.projects import ProjectDetailView
from projects.views.demo import DemoParagraphView
from projects.views.study import StudyLookupView
from projects.views.study import StudyParagraphView
from projects.views import projects

app_name = 'projects'

urlpatterns = [
    path('', projects.all_projects, name='all_projects'),
    path('<slug:slug>', ProjectDetailView.as_view(), name='detail'),
    path('demo', ProjectDetailView.as_view(), name='about_demo'),
    path('study', ProjectDetailView.as_view(), name='about_study'),
    path('exercise', ProjectDetailView.as_view(), name='about_exercise'),
    path('study/lookup', StudyLookupView.as_view(), name='study_lookup'),
    path('demo/paragraphs', DemoParagraphView.as_view(), name='demo_paragraphs'),
    path('study/paragraphs/<int:group_id>', StudyParagraphView.as_view(),
         name='study_paragraphs_with_group'),
]
