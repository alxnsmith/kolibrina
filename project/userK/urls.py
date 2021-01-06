from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import Account, Register

urlpatterns = [
    path('', login_required(Account.as_view()), name='account'),
    path('register/', Register.as_view(), name='register'),
]
