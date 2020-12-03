from django.urls import path
from .views import MarathonWeek, SummaryMarathonWeek
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('marafon-week/', login_required(MarathonWeek.as_view()), name='marafon_week'),
    path('summary-marafon-week/', login_required(SummaryMarathonWeek.as_view()), name='summary_marafon_week'),
]
