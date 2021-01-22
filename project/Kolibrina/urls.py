from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin-db/', admin.site.urls),
                  path('admin/', include('admin_panel.urls')),
                  path('', include('games.urls')),
                  path('account/', include('account.urls')),
                  path('media/', include('media.urls')),
                  path('questions/', include('questions.urls')),
                  path('rules/', include('rules.urls')),
                  path('ratings/', include('rating.urls')),
                  path('chat/', include('chat.urls')),
                  path('api/', include('API.urls')),
                  path('payment-api/', include('payment.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
