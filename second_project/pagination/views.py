import csv

import pandas as pd

from django.shortcuts import render
from django.conf import settings
from django.core.paginator import Paginator
from django.core.cache import cache


def get_data():
    data = cache.get('csv')

    if data is None:
        with open(settings.BUS_STATION_CSV) as f:
            data = f.readlines()
            reader = list(csv.DictReader(data, delimiter=','))
            cache.set('csv', reader, None)
            return reader
    return data


def bus_stations(request):
    data = get_data()
    page_number = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 10))
    per_page = max(1, min(per_page, 50))

    paginator = Paginator(data, per_page)

    page_number = max(1, min(page_number, paginator.num_pages))

    page = paginator.get_page(page_number)
    prev = page.previous_page_number() if page.has_previous() else None
    nxt = page.next_page_number() if page.has_next() else None

    df = pd.DataFrame(data=page)
    df = df.fillna(' ').T.transpose()
    df = df.to_html(index=False)

    context = {
        'page': df,
        'previous': prev,
        'next': nxt,
        'min100': page_number - 100 if page_number and page_number - 100 > 0 else None,
        'min10': page_number - 10 if page_number and page_number - 10 > 0 else None,
        'plus100': page_number + 100 if page_number and page_number + 100 < paginator.num_pages else None,
        'plus10': page_number + 10 if page_number and page_number + 10 < paginator.num_pages else None,
        'per_page': per_page,
        'page_number': page_number
    }

    return render(request, 'stations.html', context)
