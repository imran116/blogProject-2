from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse
from django.contrib.auth.models import User

from loginApp.forms import ProfileChangeForm


# Create your views here.

def blog(request):
    return render(request, 'blogApp/blog_index.html', context={'j': "hello i am form blog.page.html"})


def profile_setting(request):

    return render(request, 'blogApp/profile.html', context={})


def profile_change(request):
    current_user = request.user
    form = ProfileChangeForm(instance=current_user)
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = ProfileChangeForm(instance=current_user)

    return render(request, 'blogApp/profile_change.html', context={'form':form})
