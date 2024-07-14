from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.db.models import Q
from django.urls import reverse
from .models import Recipe, Ingredient, PreparationStep, RatingComment
from .forms import RecipeForm, IngredientFormSet, PreparationStepFormSet, RatingCommentForm


def get_breadcrumbs(items):
    breadcrumbs = []
    for item in items:
        breadcrumbs.append({
            'title': item['title'],
            'url': item.get('url', '#')
        })
    return breadcrumbs
   

def recipe_list(request):
    recipes = Recipe.objects.annotate(avg_rating=Avg('ratings__rating')).order_by('-created_at')
    breadcrumbs = get_breadcrumbs([
        {'title': 'Recipes', 'url': reverse('recipe:recipe_list')}
    ])
    context = {
        'recipes': recipes,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'recipe/recipe_list.html', context)


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ratings = recipe.ratings.all()
    avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    rating_form = RatingCommentForm()

    breadcrumbs = get_breadcrumbs([
        {'title': 'Recipes', 'url': reverse('recipe:recipe_list')},
        {'title': recipe.title}
    ])

    if request.method == 'POST':
        rating_form = RatingCommentForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.recipe = recipe
            rating.save()
            messages.success(request, "Your rating and comment have been added.")
            return redirect('recipe:recipe_detail', pk=pk)
            pass

    context = {
        'recipe': recipe,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'rating_form': rating_form,
        'breadcrumbs': breadcrumbs
    }

    return render(request, 'recipe/recipe_detail.html', context)

def search_recipes(request):
    query = request.GET.get('query', '')
    recipes = Recipe.objects.filter(
        Q(title__icontains=query) | 
        Q(description__icontains=query) |
        Q(ingredients__name__icontains=query)
    ).distinct()

    context = {
        'recipes': recipes,
        'query': query
    }
    return render(request, 'recipe/search_results.html', context) 

@login_required
def create_recipe(request):
    breadcrumbs = get_breadcrumbs([
        {'title': 'Recipes', 'url': reverse('recipe:recipe_list')},
        {'title': 'Create Recipe'}
    ])

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(request.POST, prefix='ingredients')
        step_formset = PreparationStepFormSet(request.POST, prefix='steps')
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            if 'image' in request.FILES:
                recipe.image = request.FILES['image']
            recipe.save()
            ingredient_formset.instance = recipe
            ingredient_formset.save()
            step_formset.instance = recipe
            step_formset.save()
            messages.success(request, "Recipe created successfully!")
            return redirect('recipe:recipe_detail', pk=recipe.pk)
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")
    else:
        form = RecipeForm()
        ingredient_formset = IngredientFormSet(prefix='ingredients')
        step_formset = PreparationStepFormSet(prefix='steps')
    
    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'recipe/recipe_form.html', context)

@login_required
def update_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    breadcrumbs = get_breadcrumbs([
        {'title': 'Recipes', 'url': reverse('recipe:recipe_list')},
        {'title': recipe.title, 'url': reverse('recipe:recipe_detail', args=[pk])},
        {'title': 'Edit Recipe'}
    ])

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe)
        step_formset = PreparationStepFormSet(request.POST, instance=recipe)
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = form.save(commit=False)
            if 'image' in request.FILES:
                recipe.image = request.FILES['image']
            recipe.save()
            ingredient_formset.save()
            step_formset.save()
            messages.success(request, "Recipe updated successfully!")
            return redirect('recipe:recipe_detail', pk=recipe.pk)
        else:
            messages.error(request, "There was an error with your submission. Please check the form.")
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe)
        step_formset = PreparationStepFormSet(instance=recipe)
    
    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'recipe': recipe,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'recipe/recipe_form.html', context)

@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, "Recipe deleted successfully.")
        return redirect('recipe:recipe_list')
    return render(request, 'recipe/recipe_confirm_delete.html', {'recipe': recipe})

@login_required
def rate_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        form = RatingCommentForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.recipe = recipe
            rating.save()
            messages.success(request, "Your rating and comment have been added.")
            return redirect('recipe:recipe_detail', pk=pk)
    else:
        form = RatingCommentForm()
    return render(request, 'recipe/rate_recipe.html', {'form': form, 'recipe': recipe})

@login_required
def add_to_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    request.user.userprofile.favorite_recipes.add(recipe)
    return redirect('recipe_detail', pk=recipe_id)

@login_required
def remove_from_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    request.user.userprofile.favorite_recipes.remove(recipe)
    return redirect('recipe_detail', pk=recipe_id)