from django.urls import path, include
from .views import *

urlpatterns = [
    path('', api),
    path('team/', include('teams.urls'))
]