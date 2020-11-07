from django.contrib import admin
from .models import Team


# admin.site.register(Team)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    fields = (('team_name', 'score', ), 'last_game_date')

