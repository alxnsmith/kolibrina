from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from userK.models import User, ConfirmKey


admin.site.register(ConfirmKey)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'city', 'balance', 'discount_view', 'rating', 'league', 'view_team_link')
    list_display_links = ('username',)

    readonly_fields = ('view_team_link', 'date_joined')

    search_fields = ('id', 'username', 'firstName', 'lastName', 'swPlace', 'league', 'country', 'area', 'city')
    list_filter = ('is_staff', 'is_active', 'team_role', 'groups')
    fieldsets = (
        (None, {
            'fields': (('date_joined',),
                ('username', 'hide_my_name'),
                ('firstName', 'lastName'),
                ('birthday', 'gender'),
                ('balance', 'discount'),
                ('rating', 'league')
            )
        }),
        ('Контакты', {
            'fields': (
                ('phoneNumber', 'email'),
                ('country', 'area', 'city'),
                'swPlace'
            )
        }),
        ('Команда', {
            'fields': (
                ('view_team_link', 'team_role', 'number_in_the_team'),
            )
        }),
        ('Config', {
            'fields': (
                'groups',
                ('is_staff', 'is_active'),
            )
        }),
    )

    def view_team_link(self, obj):
        html = '<a>Нет</a>'
        if obj.team_set.exists():
            team = obj.team_set.first()
            url = reverse("admin:teams_team_change", args=(f'{team.id}', ))
            html = f'<a href="{url}">{team.name}</a>'
        return format_html(html)
    view_team_link.short_description = 'Команда'

    def discount_view(self, obj):
        return f'{obj.discount}%'
    discount_view.short_description = 'Скидка'
