from django.contrib import admin

from userK.models import CustomUser, InviteList


admin.site.register(CustomUser)
admin.site.register(InviteList)
