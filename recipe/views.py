from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Recipe, RatingComment
from .forms import RecipeForm, IngredientFormSet, PreparationStepFormSet, RatingCommentForm
from django.db.models import Avg

def recipe_list(request):
    recipes = Recipe.objects.annotate(avg_rating=Avg('ratings__rating')).order_by('-created_at')
    return render(request, 'recipe/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ratings = recipe.ratings.all()
    avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
    rating_form = RatingCommentForm()

    if request.method == 'POST':
        rating_form = RatingCommentForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.user = request.user
            rating.recipe = recipe
            rating.save()
            messages.success(request, "Your rating and comment have been added.")
            return redirect('recipe:recipe_detail', pk=pk)

    context = {
        'recipe': recipe,
        'ratings': ratings,
        'avg_rating': avg_rating,
        'rating_form': rating_form,
    }
    return render(request, 'recipe/recipe_detail.html', context)

@login_required
def create_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        ingredient_formset = IngredientFormSet(request.POST)
        step_formset = PreparationStepFormSet(request.POST)
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            ingredient_formset.instance = recipe
            ingredient_formset.save()
            step_formset.instance = recipe
            step_formset.save()
            messages.success(request, "Recipe created successfully!")
            return redirect('recipe:recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
        ingredient_formset = IngredientFormSet()
        step_formset = PreparationStepFormSet()
    
    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
    }
    return render(request, 'recipe/recipe_form.html', context)

@login_required
def update_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, user=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        ingredient_formset = IngredientFormSet(request.POST, instance=recipe)
        step_formset = PreparationStepFormSet(request.POST, instance=recipe)
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            form.save()
            ingredient_formset.save()
            step_formset.save()
            messages.success(request, "Recipe updated successfully!")
            return redirect('recipe:recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
        ingredient_formset = IngredientFormSet(instance=recipe)
        step_formset = PreparationStepFormSet(instance=recipe)
    
    context = {
        'form': form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset,
        'recipe': recipe,
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
