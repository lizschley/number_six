''' home urls (accessed directly from base url) '''
from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('resume', views.resume, name='resume'),
]
