from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient, PreparationStep, RatingComment


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "description",
            "image",
            "category",
            "cook_time",
            "prep_time",
        ]  # noqa


IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    fields=["name", "quantity", "unit"],
    extra=1,
    can_delete=True,  #  noqa
)

PreparationStepFormSet = inlineformset_factory(
    Recipe,
    PreparationStep,
    fields=["step_number", "description"],
    extra=1,
    can_delete=True,
)


class RatingCommentForm(forms.ModelForm):
    class Meta:
        model = RatingComment
        fields = ["rating", "comment"]
