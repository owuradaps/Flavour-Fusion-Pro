from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('<int:pk>/update/', views.update_recipe, name='update_recipe'),
    path('<int:pk>/delete/', views.delete_recipe, name='delete_recipe'),
    path('<int:pk>/rate/', views.rate_recipe, name='rate_recipe'),
    path('<int:recipe_id>/favorite/', views.add_to_favorites, name='add_to_favorites'),
    path('<int:recipe_id>/unfavorite/', views.remove_from_favorites, name='remove_from_favorites'),
    path('search/', views.search_recipes, name='search_recipes'),
]