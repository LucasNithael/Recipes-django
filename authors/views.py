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
    request.session['request_form_data'] = POST
    form = RegisterForm(POST)

    return redirect('authors:register')
