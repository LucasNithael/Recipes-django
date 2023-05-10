from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.http import Http404


def register_view(request):
    request_form_data = request.session.get('request_form_data')
    form = RegisterForm(request_form_data)
    return render(request, 'authors/pages/register_view.html', {'form': form})


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
        form.save()
        messages.success(request, 'Your use is created, you can login')
        '''
        limpa os dados da sessão caso o formulário seja válidado
        '''
        del (request.session['request_form_data'])

    return redirect('authors:register')
