from django.urls import path
from projects.views import ProjectDetailView
from projects.views import ProjectDemoView
from projects import views


app_name = 'projects'

urlpatterns = [
    path('', views.all_projects, name='all_projects'),
    path('<slug:slug>', ProjectDetailView.as_view(), name='detail'),
    path('demo', ProjectDemoView.as_view(), name='demo_landing_page'),
    path('study', ProjectDemoView.as_view(), name='study_landing_page'),
    path('exercise', ProjectDemoView.as_view(), name='exercise_landing_page'),
]