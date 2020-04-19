from django.shortcuts import render
# from home.models import Home


def home(request):
    return render(request, 'home/home.html')