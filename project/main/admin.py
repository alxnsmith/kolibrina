from django.contrib import admin

from django.contrib.auth.models import Group
from userK.models import CustomUser
from rules.models import Rule
from addquestion.models import Questions, Theme, Category, Purpose

admin.site.unregister(Group)
admin.site.register(CustomUser)
admin.site.register(Questions)
admin.site.register(Theme)
admin.site.register(Category)
admin.site.register(Purpose)
# admin.site.register(Rule)