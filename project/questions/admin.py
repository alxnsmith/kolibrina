from django.contrib import admin

from questions.models import Questions, Theme, Category, Purpose

# Register your models here.

admin.site.register(Questions)
admin.site.register(Theme)
admin.site.register(Category)
admin.site.register(Purpose)
