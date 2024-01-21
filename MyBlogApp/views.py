from django.shortcuts import HttpResponseRedirect,HttpResponse
from django.urls import reverse


def Index(request):
    return HttpResponseRedirect(reverse('blog_app:blog_home'))
