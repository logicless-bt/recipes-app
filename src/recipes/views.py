from django.shortcuts import render, get_object_or_404
from .models import Recipe
from django.contrib.auth.decorators import login_required #authentication

# Create your views here.
def home(request):
    return render(request, "recipes/home.html")
@login_required
def recipe_details(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_details.html', {'recipes': recipes})
@login_required
def recipe_indiv(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe.separate_ingredients_by_comma()    # split ingredients list
    recipe.calculate_difficulty()             # update difficulty
    recipe.save()                              
    return render(request, 'recipes/recipe_indiv.html', {'recipe': recipe})