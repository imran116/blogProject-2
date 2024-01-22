from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from loginApp.forms import UserForm

from django.contrib.auth.models import User


# Create your views here.

def register_view(request):
    form = UserForm()
    register = False
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if form.is_valid():
            form.save()
            register = True

    context = {
        'form': form,
        'register': register,
    }
    return render(request, 'loginApp/register.html', context=context)


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

    return render(request, 'loginApp/login.html', context={'form': form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))




