from django.shortcuts import render

from .models import Article


def articles_list(request):
    template = 'articles/news.html'
    context = {'object_list': Article.objects.all()}

    return render(request, template, context)
