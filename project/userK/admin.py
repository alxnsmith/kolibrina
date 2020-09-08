from django.contrib import admin

from userK.models import CustomUser, TeamInvites


admin.site.register(CustomUser)
admin.site.register(TeamInvites)
