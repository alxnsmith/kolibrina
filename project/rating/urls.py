from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import ratings, SummaryMarathonWeek

urlpatterns = [
    path('', ratings, name='ratings'),
    path('summary-marafon-week-<int:id>/', login_required(SummaryMarathonWeek.as_view()), name='summary_marafon_week'),

]
