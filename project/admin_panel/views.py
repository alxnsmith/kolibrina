from django.shortcuts import render, get_list_or_404
from django.http.response import Http404
from django.views import View


class AdminPanel(View):
    def get(self, request):
        if not request.user.is_staff:
            raise Http404
        return render(request, 'admin_panel/index.html')
