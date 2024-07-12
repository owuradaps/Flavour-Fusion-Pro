from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, Ingredient, PreparationStep, RatingComment

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'image', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'category': forms.Select(choices=Recipe.CATEGORY_CHOICES),
            'image': forms.ClearableFileInput(attrs={'accept': 'image/*'}),  # Add this line
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control-file'})  # Add this methods

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']
        widgets = {
            'quantity': forms.NumberInput(attrs={'step': '0.01'}),
        }

class PreparationStepForm(forms.ModelForm):
    class Meta:
        model = PreparationStep
        fields = ['step_number', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class RatingCommentForm(forms.ModelForm):
    class Meta:
        model = RatingComment
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

IngredientFormSet = inlineformset_factory(
    Recipe, 
    Ingredient, 
    form=IngredientForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)

PreparationStepFormSet = inlineformset_factory(
    Recipe, 
    PreparationStep, 
    form=PreparationStepForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)