from django.shortcuts import HttpResponseRedirect,HttpResponse
from django.urls import reverse


def Index(request):
    return HttpResponse("hello world.")
