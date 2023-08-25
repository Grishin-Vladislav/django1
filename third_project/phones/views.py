from django.shortcuts import render, redirect
from django.http import Http404

from django.core.exceptions import ObjectDoesNotExist
from .models import Phone


def index(request):
    return redirect('catalogue')


def show_catalog(request):
    sort: str = request.GET.get('sort')
    phones: list = list(Phone.objects.all())

    if sort == 'name':
        phones.sort(key=lambda x: x.name)
    elif sort == 'min_price':
        phones.sort(key=lambda x: x.price)
    elif sort == 'max_price':
        phones.sort(key=lambda x: x.price, reverse=True)

    context = {
        'phones': phones
    }
    return render(request, 'home.html', context=context)


def show_phone(request, slug):
    try:
        phone = Phone.objects.get(slug=slug)
        context = {
            'phone': phone
        }
        return render(request, 'phone.html', context=context)
    except ObjectDoesNotExist:
        raise Http404()
