from django.shortcuts import render, redirect, HttpResponse
from . import forms
from django.views.generic.edit import FormView
from base64 import b64encode
from main.sendmail import sendmail


class Register(FormView):
    form_class = forms.RegForm
    success_url = "/auth/login/"
    template_name = "regK/register.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('account')
        return super(Register, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        DOMAIN = self.request.META['HTTP_HOST']
        confirmUrl = 'http://' + DOMAIN + r'/accountconfirmation/account/email?c=' + b64encode(email.encode('utf-8')).decode("utf-8")
        messageText = f'Ваша ссылка для активации аккаунта: \n %s' % confirmUrl
        sendmail('Активация аккаунта', messageText, email)
        return super(Register, self).form_valid(form)

    def form_invalid(self, form):
        return super(Register, self).form_invalid(form)