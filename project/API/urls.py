from django.urls import path, include
from .views import *

urlpatterns = [
    path('', api, name='API'),
    path('team/', include('api_teams.urls'))
]