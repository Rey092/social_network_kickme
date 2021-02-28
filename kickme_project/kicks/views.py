from django.shortcuts import render
from django.http import HttpResponse
from .models import Kick


def home_view(request, *args, **kwargs):
    print(args, kwargs)
    return HttpResponse("<h1>Hello World</h1>")
