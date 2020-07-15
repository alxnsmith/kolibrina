from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('regK.urls')),
    path('account/', include('userK.urls')),
    path('auth/', include('authK.urls')),
    path('media/', include('media.urls')),
    path('media/', include('media.urls')),
    path('accountconfirmation/', include('accountConfirmation.urls')),
    path('questions/', include('questions.urls')),
    path('add-question/', include('addquestion.urls')),
    path('rules/', include('rules.urls')),
    path('chat/', include('chat.urls')),
    path('', include('game.urls')),
]