from django.urls import path
from .views import MarathonWeek
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('marafon-week/', login_required(MarathonWeek.as_view()), name='marafon_week'),
]
