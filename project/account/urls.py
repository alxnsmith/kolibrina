from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import Account, Register, ConfirmAccount, Logout, Login

urlpatterns = [
    path('', login_required(Account.as_view()), name='account'),
    path('register/', Register.as_view(), name='register'),
    path('confirm/', ConfirmAccount.as_view(), name='confirm_account'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', login_required(Logout.as_view()), name='logout'),
]
