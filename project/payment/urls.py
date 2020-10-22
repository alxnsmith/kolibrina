from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', csrf_exempt(views.PaymentAPI.as_view()), name='PaymentAPI'),
    path('adw3re4t5y6u7iuuyjtrge4w3r4t5y7jukiyjthrgefwdqs2wd3efrgt54yh6uyjtrge4w3r4t5y7jukiyjt',
         csrf_exempt(views.Notifications.as_view()),
         name='Notifications'),
]