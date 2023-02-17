from django.shortcuts import render
from utils.recipes.gerador import make_recipe


def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'recipes': [make_recipe() for _ in range(10)],
    })


def recipe(request, pk):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': make_recipe(),
        'is_detail_page': True,
    })