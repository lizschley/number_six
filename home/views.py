from django.shortcuts import render


def home(request):
    return render(request, 'home/home.html')


def resume(request):
    return render(request, 'home/resume.html')
