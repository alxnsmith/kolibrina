from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import Account

urlpatterns = [
    path('', login_required(Account.as_view()), name='account'),
]
