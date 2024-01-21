from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.urls import reverse
from django.contrib.auth.models import User


# Create your views here.

def blog(request):
    return render(request, 'blogApp/blog_index.html', context={'j': "hello i am form blog.page.html"})


def profile_setting(request):

    return render(request, 'blogApp/profile.html', context={})
