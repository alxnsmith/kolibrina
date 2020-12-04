from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils import timezone

from .models import MarathonRound, MarathonWeekOfficial, MarathonWeekCommunity, \
    MarathonThemeBlock

admin.site.register(MarathonWeekCommunity)


@admin.register(MarathonRound)
class MarathonRoundAdmin(admin.ModelAdmin):
    def get_instance(self, request):
        id = request.scope['path'].split('/')[-3]
        return self.get_object(request, id)

    def themes(self, obj):
        return ', '.join([block.theme.theme for block in obj.question_blocks.all()])
    themes.short_description = 'Темы'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'starter_player':
            marathon = self.get_instance(request)
            if marathon:
                kwargs['queryset'] = marathon.players.all()
        return super(MarathonRoundAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'question_blocks':
            round = self.get_instance(request)
            queryset = MarathonThemeBlock.objects.none()
            all_blocks = MarathonThemeBlock.objects.all()
            for block in all_blocks:
                if not block.marathonround_set.all().exists():
                    queryset |= MarathonThemeBlock.objects.filter(pk=block.pk)
            if round:
                for block in round.question_blocks.all():
                    queryset |= MarathonThemeBlock.objects.filter(pk=block.pk)
            kwargs['queryset'] = queryset
        return super(MarathonRoundAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    list_display = ('id', 'themes', 'date_time_start', 'create_date', 'is_played')
    list_display_links = ('themes',)
    readonly_fields = ('is_played', )


@admin.register(MarathonWeekOfficial)
class MarathonWeekOfficialAdmin(admin.ModelAdmin):
    list_display = ('code_name', 'is_rating', 'is_active', 'rounds_display')
    readonly_fields = ('create_date',)

    def rounds_display(self, obj):
        if obj.rounds.exists():
            to_display = []
            for round in obj.rounds.all().order_by('date_time_start'):
                url = reverse('admin:marathon_marathonround_change', args=(f'{round.pk}', ))
                style = 'style="color: lime"' if round.is_played else ''
                text = 'None'
                if date_time_start := timezone.localtime(round.date_time_start):
                    day = str(date_time_start.day).rjust(2, '0')
                    month = str(date_time_start.month).rjust(2, '0')
                    year = str(date_time_start.year).rjust(2, '0')
                    hour = str(date_time_start.hour).rjust(2, '0')
                    minute = str(date_time_start.minute).rjust(2, '0')
                    second = str(date_time_start.second).rjust(2, '0')
                    text = f'{day}/{month}/{str(year)[:2]} в {hour}:{minute}:{second}'

                html = f'<a href="{url}" {style}>{text}</a>'
                to_display.append(html)
            return format_html(' | '.join(to_display))
        else:
            return 'Empty'
    rounds_display.short_description = 'Раунды'

    def get_instance(self, request):
        id = request.scope['path'].split('/')[-3]
        return self.get_object(request, id)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'rounds':
            marathon = self.get_instance(request)
            queryset = MarathonRound.objects.none()
            all_rounds = MarathonRound.objects.all()
            for round in all_rounds:
                if not round.official_marathon_round_set.all().exists() \
                        and not round.marathonweekcommunity_set.all().exists():
                    queryset |= MarathonRound.objects.filter(pk=round.pk, is_active=True)
            if marathon:
                for round in marathon.rounds.all():
                    queryset |= MarathonRound.objects.filter(pk=round.pk)
            kwargs['queryset'] = queryset
        return super(MarathonWeekOfficialAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
