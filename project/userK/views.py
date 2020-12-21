from django.shortcuts import render, redirect
from django.views import View
from . import services


class Account(View):
    def get(self, request):
        return render(request, 'userK/account.html', self.render_data)

    def post(self, request):
        data = services.create_render_data(request)
        result = services.write_user_model(request.user, request.POST)
        if result['status'] == 'OK':
            return redirect('account')
        elif result['status'] == 'error':
            error = {'error': result['error']}
            data['errors'].append(error)
            return render(request, 'userK/account.html', self.render_data)

    @property
    def render_data(self):
        return services.create_render_data(self.request)
