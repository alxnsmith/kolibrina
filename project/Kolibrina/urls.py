from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('regK.urls')),
    path('account/', include('userK.urls')),
    path('auth/', include('authK.urls')),
    path('media/', include('media.urls')),
    path('media/', include('media.urls')),
    path('accountconfirmation/', include('accountConfirmation.urls')),
    path('questions/', include('questions.urls')),
    path('rules/', include('rules.urls')),
    path('ratings/', include('rating.urls')),
    path('chat/', include('chat.urls')),
    path('', include('game.urls')),
    path('api/', include('API.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
