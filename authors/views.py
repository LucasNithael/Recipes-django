from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegisterForm
from django.http import Http404


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

    return redirect('authors:register')


def login_view(request):
    return render(request, 'authors/pages/login.html')