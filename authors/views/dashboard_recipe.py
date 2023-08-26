from django.views import View
from authors.forms import AuthorRecipeForm
from recipes.models import Recipe
from django.http.response import Http404
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect


class DashboardRecipe(View):
    def get(self, request, id):
        recipe = Recipe.objects.filter(
            is_published=False,
            author=request.user,
            pk=id
        ).first()

        if not recipe:
            raise Http404
        
        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso')
            return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

        return render(request, 'authors/pages/dashboard_recipe.html', {
            'form': form,
        })
