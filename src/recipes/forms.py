from django import forms
from .models import Recipe
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

CHART__CHOICES = (          
   ('#1', 'Bar chart'),    # when user selects "Bar chart", it is stored as "#1"
   ('#2', 'Pie chart'),
   ('#3', 'Line chart')
)

#define class-based form (imported)
class RecipeSearchForm(forms.Form): 
   recipe_name = forms.CharField(max_length=120)
   chart_type = forms.ChoiceField(choices=CHART__CHOICES)

class RecipeForm(forms.ModelForm):
   class Meta:
      model = Recipe
      fields = ['name', 'ingredients', 'cooking_time', 'description', 'pic']
      widgets = {
         'description': forms.Textarea(attrs={'rows': 4}),
      }

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']