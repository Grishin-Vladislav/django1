import os

from django.shortcuts import render, reverse


def home_view(request):
    template_name = 'app/home.html'

    pages = {
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }

    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):

    template = 'app/time.html'
    context = {'home': reverse('home')}

    return render(request, template, context)


def workdir_view(request):

    template = 'app/dirs.html'
    dirs = os.listdir()

    context = {
        'dirs': dirs,
        'home': reverse('home')
    }

    return render(request, template, context)
