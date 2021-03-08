from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
import random
from .models import Kick
from .forms import KickForm
from django.conf import settings

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, "kicks/home.html", context={}, status=200)


def kick_list_view(request, *args, **kwargs):
    qs = Kick.objects.all()
    kicks_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": kicks_list
    }
    return JsonResponse(data)


def kick_create_view(request, *args, **kwargs):
    form = KickForm(request.POST or None)
    next_url = request.POST.get('next') or None
    if form.is_valid():
        obj = form.save(commit=False)   
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url is not None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = KickForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form": form})


def kick_detail_view(request, kick_id, *args, **kwargs):
    """
    REST API VIEW
    Consume by .JS
    return .json
    """

    data = {
        "id": kick_id,
    }
    status = 200
    try:
        obj = Kick.objects.get(id=kick_id)
        data['content'] = obj.content
    except NameError:
        data['message'] = "Not found"
        status = 404
    return JsonResponse(data, status=status)
