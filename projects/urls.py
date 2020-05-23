from django.urls import path
from projects.views import ProjectDetailView
from projects.view_dir.demo.demo_paragraphs import ProjectDemoParagraphView
from projects import views


app_name = 'projects'

urlpatterns = [
    path('', views.all_projects, name='all_projects'),
    path('<slug:slug>', ProjectDetailView.as_view(), name='detail'),
    path('demo', ProjectDetailView.as_view(), name='demo_landing_page'),
    path('study', ProjectDetailView.as_view(), name='study_landing_page'),
    path('exercise', ProjectDetailView.as_view(), name='exercise_landing_page'),
    path('view_dir/demo/demo_paragraphs', ProjectDemoParagraphView.as_view(), name='demo_paragraphs'),
]