from django.contrib import admin
from .models import TournamentWeekScoreUserLink, ScoreHistoryElement, MarathonWeekScoreUserLink

admin.site.register((ScoreHistoryElement, TournamentWeekScoreUserLink))


@admin.register(MarathonWeekScoreUserLink)
class MarathonWeekScoreUserLinkAdmin(admin.ModelAdmin):
    list_display = ('round_instance', 'marathon_id', 'user_instance', 'score_instance')
    sortable_by = ('round_instance', 'user_instance', 'score_instance')

    def user_instance(self, obj):
        return obj.score_instance.player
    user_instance.short_description = 'Игрок'

    def marathon_id(self, obj):
        if marathon := obj.round_instance.marathonweekofficial_set.first():
            return marathon.id
    marathon_id.short_description = 'ID марафона'
