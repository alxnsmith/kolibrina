from django.contrib import admin
from django.urls import path, re_path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', include('regK.urls')),
    path('account/', include('userK.urls')),
    path('auth/', include('authK.urls')),

    re_path('accountconfirmation/', include('accountConfirmation.urls')),
]
