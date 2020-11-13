from django.contrib import admin

from .models import TournamentScoreUserLink, Attempt, Tournament

admin.site.register(TournamentScoreUserLink)
admin.site.register(Attempt)
admin.site.register(Tournament)
