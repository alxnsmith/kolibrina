from django.contrib import admin
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter, SimpleDropdownFilter
from rangefilter.filter import DateTimeRangeFilter

from questions.models import Question, Theme, Category, Purpose, MarathonThemeBlock

# Register your models here.

admin.site.register(Theme)
admin.site.register(Category)
admin.site.register(Purpose)
admin.site.register(MarathonThemeBlock)


class DateDropdownFilter(admin.DateFieldListFilter):
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'


class DropdownBooleanFieldFilter(admin.BooleanFieldListFilter):
    # pass
    template = 'Kolibrina/admin/blocks/dropdown_boolean_filter.html'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    # class CategoryFilter(SimpleDropdownFilter):
    #     """Делает то же самое, что и ('theme__category', RelatedFieldListFilter),
    #     но не отображает пустые категории."""
    #
    #     title = 'Категория'
    #     parameter_name = 'category'
    #
    #     def lookups(self, request, model_admin):
    #         categories = set([question.theme.category for question in model_admin.model.objects.all()])
    #         return [(category.id, category.category) for category in categories]
    #
    #     def queryset(self, request, queryset):
    #         if self.value():
    #             return queryset.filter(theme__category=self.value())

    def category(self, obj):
        return obj.theme.category

    category.short_description = 'Категория'

    def short_correct_answer(self, obj):
        return obj.correct_answer

    short_correct_answer.short_description = 'Ответ'

    def short_question(self, obj):
        limit = 50
        question = obj.question
        if len(question) > limit:
            question = question[:limit] + '...'

        return question

    short_question.short_description = 'Вопрос'

    list_display_links = ('short_question',)
    readonly_fields = ('create_date',)
    list_display = ('id', 'short_question', 'short_correct_answer', 'category', 'theme', 'create_date',)
    search_fields = ('question', 'correct_answer', 'theme__theme', 'difficulty')

    list_filter = (
        ('purpose', RelatedDropdownFilter),
        ('public', DropdownBooleanFieldFilter),
        ('moderate', DropdownBooleanFieldFilter),
        ('theme', RelatedDropdownFilter),
        ('theme__category', RelatedDropdownFilter),
        ('author', RelatedDropdownFilter),
        ('create_date', DateDropdownFilter),
        ('create_date', DateTimeRangeFilter),
    )
