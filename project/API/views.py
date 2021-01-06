from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from account.models import User as User


def api(request):
    sender_name = str(request.user)
    user = get_object_or_404(User, username=sender_name)

    def get_contains(req):
        return req in request.GET

    response = {}
    if get_contains('username'):
        response['username'] = sender_name
    if get_contains('userstatus'):
        response['userstatus'] = {}
        response['userstatus']['admin'] = user.is_staff
        response['userstatus']['is_active'] = user.is_active
    if get_contains('balance'):
        response['balance'] = user.balance

    if response != {}:
        return JsonResponse(response)
    else:
        return Http404
