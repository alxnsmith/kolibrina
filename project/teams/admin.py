from django.contrib import admin

from .models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    fields = (('name', 'score',), 'last_game_date', 'players')
