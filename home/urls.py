''' home urls (accessed directly from base url) '''
from django.urls import path
from home import views
from home.views import ResumeView

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('resume', ResumeView.as_view(), name='resume'),
]
