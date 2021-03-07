from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
import random
from .models import Kick
from .forms import KickForm


def home_view(request, *args, **kwargs):
    return render(request, "kicks/home.html", context={}, status=200)


def kick_list_view(request, *args, **kwargs):
    qs = Kick.objects.all()
    kicks_list = [{"id": x.id, "content": x.content, "likes": random.randint(1, 120)} for x in qs]
    data = {
        "isUser": False,
        "response": kicks_list
    }
    return JsonResponse(data)


def kick_create_view(request, *args, **kwargs):
    form = KickForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        form = KickForm()
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
