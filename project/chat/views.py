from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from media.services import get_banner


# def chat(request):
#     main_banner = get_banner()
#     return render(request, 'chat/chat.html', {
#         'mainBanner': main_banner,
#         })


class Chat(LoginRequiredMixin, View):
    def get(self, request):
        main_banner = get_banner()
        return render(request, 'chat/chat.html', {
            'mainBanner': main_banner,
        })
