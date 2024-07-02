from django.contrib import admin
from .models import Recipe, Ingredient, PreparationStep, RatingComment

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(PreparationStep)
admin.site.register(RatingComment)
