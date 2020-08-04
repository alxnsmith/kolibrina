from django.shortcuts import render
from .models import Rule


def rules(request):
    rulesList = Rule.objects.extra(select={'order': 'CAST(orderRules AS INTEGER)'}).order_by('order')

    return render(request, 'rules/rules.html', {'rules': rulesList})
