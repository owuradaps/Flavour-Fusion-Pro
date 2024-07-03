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
]