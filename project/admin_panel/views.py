from django.shortcuts import render
from django.views import View


class AdminPanel(View):
    def get(self, request):
        return render(request, 'admin_panel/index.html')
