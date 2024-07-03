
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']

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
        }

# Formsets
IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient, form=IngredientForm,
    extra=1, can_delete=True, min_num=1, validate_min=True
)

PreparationStepFormSet = inlineformset_factory(
    Recipe, PreparationStep, form=PreparationStepForm,
    extra=1, can_delete=True, min_num=1, validate_min=True
)