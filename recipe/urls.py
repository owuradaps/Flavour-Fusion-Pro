from django.urls import path
from . import views

app_name = "recipe"

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path("create/", views.create_recipe, name="create_recipe"),
    path("<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("<int:pk>/edit/", views.update_recipe, name="update_recipe"),
    path("<int:pk>/delete/", views.delete_recipe, name="delete_recipe"),
    path("search/", views.search_recipes, name="search_recipes"),
    path("<int:pk>/rate/", views.rate_recipe, name="rate_recipe"),
    path(
        "<int:recipe_id>/add-to-favorites/",
        views.add_to_favorites,
        name="add_to_favorites",
    ),
    path(
        "<int:recipe_id>/remove-from-favorites/",
        views.remove_from_favorites,
        name="remove_from_favorites",
    ),
]
