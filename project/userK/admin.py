from django.contrib import admin

from userK.models import CustomUser, InviteToTeam


admin.site.register(CustomUser)
admin.site.register(InviteToTeam)
