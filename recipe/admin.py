from django.contrib import admin
from .models import Recipe, Ingredient, PreparationStep, RatingComment

class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1

class PreparationStepInline(admin.TabularInline):
    model = PreparationStep
    extra = 1

class RatingCommentInline(admin.TabularInline):
    model = RatingComment
    extra = 0

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'user__username')
    inlines = [IngredientInline, PreparationStepInline, RatingCommentInline]

# Only register these if you want them to have their own admin pages
# admin.site.register(Ingredient)
# admin.site.register(PreparationStep)
# admin.site.register(RatingComment)
