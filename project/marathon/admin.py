from django.contrib import admin

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

    list_display = ('themes', 'id', 'create_date')


@admin.register(MarathonWeekOfficial)
class MarathonWeekOfficialAdmin(admin.ModelAdmin):
    list_display = ('code_name', 'is_rating', 'is_active', 'price', 'date_time_start')
    readonly_fields = ('create_date',)

    def get_instance(self, request):
        id = request.scope['path'].split('/')[-3]
        return self.get_object(request, id)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'starter_player':
            marathon = self.get_instance(request)
            if marathon:
                kwargs['queryset'] = marathon.players.all()
        return super(MarathonWeekOfficialAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'rounds':
            marathon = self.get_instance(request)
            queryset = MarathonRound.objects.none()
            all_rounds = MarathonRound.objects.all()
            for round in all_rounds:
                if not round.marathonweekofficial_set.all().exists() \
                        and not round.marathonweekcommunity_set.all().exists():
                    queryset |= MarathonRound.objects.filter(pk=round.pk)
            if marathon:
                for round in marathon.rounds.all():
                    queryset |= MarathonRound.objects.filter(pk=round.pk)
            print(queryset)
            kwargs['queryset'] = queryset
        return super(MarathonWeekOfficialAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
