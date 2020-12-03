from django.contrib import admin

from .models import ScoreHistoryElement, RatingHistoryElement

admin.site.register((ScoreHistoryElement, RatingHistoryElement))
