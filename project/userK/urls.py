from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import Account, Register, ConfirmAccount

urlpatterns = [
    path('', login_required(Account.as_view()), name='account'),
    path('register/', Register.as_view(), name='register'),
    path('confirm/', ConfirmAccount.as_view(), name='confirm_account'),
]
