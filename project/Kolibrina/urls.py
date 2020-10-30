from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin-db/', admin.site.urls),
    path('admin/', include('admin_panel.urls')),
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
    path('', include('games.urls')),
    path('api/', include('API.urls')),
    path('payment-api/', include('payment.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
