from django.http import JsonResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404
from userK.models import CustomUser as User


def api(request):
    sender_name = str(request.user)
    user = get_object_or_404(User, username=sender_name)
    def value(req):
       return request.GET.__contains__(req)

    response = {}
    if value('username'):
        response['username'] = sender_name
    if value('userstatus'):
        response['userstatus'] = {}
        response['userstatus']['admin'] = user.is_staff
        response['userstatus']['is_active'] = user.is_active

    if response != {}:
        return JsonResponse(response)
    else:
        return Http404
