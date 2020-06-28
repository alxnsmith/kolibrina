from django.shortcuts import render
from . import forms
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from base64 import b64encode


class Register(FormView):
    form_class = forms.RegForm
    success_url = "/login/"
    template_name = "regK/register.html"

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get('email')
        DOMAIN = 'http://127.0.0.1:8000/'
        confirmUrl = DOMAIN + r'accountconfirmation/account/email?c=' + b64encode(email.encode('utf-8')).decode("utf-8")
        messageText = f'Ваша ссылка для активации аккаунта: \n %s' % confirmUrl
        send_mail('Активация аккаунта', messageText, 'kotovvsan@ya.ru',
                  [email], fail_silently=False)
        return super(Register, self).form_valid(form)

    def form_invalid(self, form):
        return super(Register, self).form_invalid(form)
