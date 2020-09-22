from django.contrib import admin

from questions.models import Question, Theme, Category, Purpose

# Register your models here.

admin.site.register(Question)
admin.site.register(Theme)
admin.site.register(Category)
admin.site.register(Purpose)
