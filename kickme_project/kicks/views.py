from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse

from .models import Kick


def home_view(request, *args, **kwargs):
    return render(request, "kicks/home.html", context={}, status=200)


def kick_list_view(request, *args, **kwargs):
    qs = Kick.objects.all()
    kicks_list = [{"id": x.id, "content": x.content} for x in qs]
    data = {
        "response": kicks_list
    }
    return JsonResponse(data)


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
    return JsonResponse(data, status=status)  # json.dumps