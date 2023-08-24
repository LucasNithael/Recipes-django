from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm, AuthorRecipeForm
from django.contrib.auth.decorators import login_required
from recipes.models import Recipe


def register_view(request):
    request_form_data = request.session.get('request_form_data')
    form = RegisterForm(request_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:create')
    })


def register_create(request):
    if not request.POST:
        raise Http404

    POST = request.POST
    '''
    Guarda os dados do form na sessão do navegador
    '''
    request.session['request_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        ''' Cria uma instancia de objeto com os dados fornecidos no forms sem o
         salvar no banco de dados'''
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Your use is created, you can login')
        # limpa os dados da sessão caso o formulário seja váliado
        del (request.session['request_form_data'])

    return redirect('authors:login')


def login_view(request):
    form = LoginForm()
    action = reverse('authors:login_create')
    context = {'form': form, 'form_action': action}
    return render(request, 'authors/pages/login.html', context)


def login_create(request):
    if request.method != 'POST':
        raise Http404

    form = LoginForm(request.POST)

    if form.is_valid():
        username = form.cleaned_data.get('username', '')
        password = form.cleaned_data.get('password', '')
        authenticate_user = authenticate(username=username, password=password)
        if authenticate_user is not None:
            messages.success(request, 'Successs')
            login(request, authenticate_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect('authors:dashboard')


# apenas usuários logados podem acessa essa view                            
@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect('authors:login')

    logout(request)
    return redirect('authors:login')


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard(request):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(request, 'authors/pages/dashboard.html', {
        'recipes': recipes
    })


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit(request, id):
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


def recipe_delete(request, id):
    if request.method != 'POST':
        raise Http404
    
    recipe = Recipe.objects.filter(
        pk=id,
        author=request.user,
        is_published=False,
        ).first()

    if recipe:
        recipe.delete()
        messages.success(request, 'Receita deletada com sucesso')
    else:
        messages.error(request, 'Erro ao deletar receita')
    
    return redirect('authors:dashboard')


