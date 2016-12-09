

from django.shortcuts import render


def index(request):
    context = {'user': request.user}
    return render(request, 'index.html', context)


def home(request):
    context = {'user': request.user}
    return render(request, 'home.html', context)
