''' urls.py is standard django '''
from django.urls import path
from projects.views.projects import ProjectDetailView
from projects.views.demo import DemoParagraphView
from projects.views.study import StudyLookupView, StudyParagraphView
from projects.views.flashcard import FlashcardView
# from projects.views.study import para_by_subtitle
from projects.views.demo import para_by_subtitle
from projects.views import projects

app_name = 'projects'

urlpatterns = [
    path('', projects.all_projects, name='all_projects'),
    path('<slug:slug>', ProjectDetailView.as_view(), name='detail'),
    path('<slug:exercise>', ProjectDetailView.as_view(), name='exercise'),
    path('demo', ProjectDetailView.as_view(), name='about_demo'),
    path('study', ProjectDetailView.as_view(), name='about_study'),
    path('exercise', ProjectDetailView.as_view(), name='about_exercise'),
    path('study/lookup', StudyLookupView.as_view(), name='study_lookup'),
    path('demo/paragraphs', DemoParagraphView.as_view(), name='demo_paragraphs'),
    path('study/paragraphs/<int:group_id>', StudyParagraphView.as_view(),
         name='study_paragraphs_with_group'),
    path('study/paragraphs/para_by_subtitle', para_by_subtitle, name='study_para_by_subtitle'),
    path('study/paragraphs/flashcards/<int:category_id>', FlashcardView.as_view(),
         name='study_paragraphs_with_category'),

]
