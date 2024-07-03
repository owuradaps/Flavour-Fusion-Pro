from django.contrib import admin
from .models import Recipe, Ingredient, PreparationStep

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class PreparationStepInline(admin.TabularInline):
    model = PreparationStep
    extra = 1

# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     inlines = [IngredientInline, PreparationStepInline]
#     list_display = ('title', 'user', 'category', 'created_at')
#     list_filter = ('category', 'created_at')
#     search_fields = ('title', 'description', 'user__username')
