from django.contrib import admin

from .models import MarathonRound, MarathonWeekOfficial, MarathonWeekCommunity

admin.site.register(MarathonRound)
admin.site.register(MarathonWeekCommunity)


@admin.register(MarathonWeekOfficial)
class MarathonWeekOfficialAdmin(admin.ModelAdmin):
    list_display = ('code_name', 'is_rating', 'is_active', 'price', 'date_time_start')