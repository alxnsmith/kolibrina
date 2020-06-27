from django.shortcuts import render
from . import forms
from django.views.generic.edit import FormView


class Register(FormView):
    form_class = forms.RegForm
    success_url = "/login/"
    template_name = "regK/register.html"

    def form_valid(self, form):
        form.save()
        return super(Register, self).form_valid(form)

    def form_invalid(self, form):
        return super(Register, self).form_invalid(form)
