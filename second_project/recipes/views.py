from copy import copy

import django.http
from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    }
}


def show_recipes(request, recipe_name):
    context = dict()
    context['recipe'] = copy(DATA.get(recipe_name))

    if not context['recipe']:
        raise django.http.Http404

    servings = int(request.GET.get('servings', 1))

    if not (1 < servings < 10000):
        servings = 1

    for ingredient_name in context['recipe']:
        context['recipe'][ingredient_name] *= servings

    context['title'] = f'recipe of {recipe_name}'

    return render(request, 'stations.html', context)
