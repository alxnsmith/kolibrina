from django.shortcuts import render, HttpResponse
from django.views import View


class AdminPanel(View):
    def get(self, request):
        return HttpResponse('Hello from admin panel')
