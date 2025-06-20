from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe
from .forms import RecipeSearchForm, RecipeForm, SignUpForm
import pandas as pd
from django.contrib.auth.decorators import login_required #authentication
from .utils import get_recipename_from_id, get_chart

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
@login_required
def search(request):
    form = RecipeSearchForm(request.POST or None)
    recipe_df = None
    recipe_name = None
    chart = None

    if request.method == 'POST':
        recipe_name = request.POST.get('recipe_name')
        chart_type = request.POST.get('chart_type')
        
        qs = Recipe.objects.filter(name=recipe_name)
        if qs:
            df = pd.DataFrame(qs.values('id', 'name', 'ingredients', 'cooking_time', 'difficulty', 'description', 'pic'))
            df['id'] = df['id'].apply(get_recipename_from_id)

            chart = get_chart(chart_type, df)
            recipe_df = df.to_html()

    context = {
        'form': form,
        'recipe_df': recipe_df,
        'chart': chart,
    }
    return render(request, 'recipes/search.html', context)

@login_required
def charts(request):
    recipes = Recipe.objects.all()

    # Difficulty Pie Chart
    difficulties = recipes.values_list('difficulty', flat=True)
    difficulty_counts = pd.Series(difficulties).value_counts()

    # Generate charts
    difficulty_chart = get_chart('pie', difficulty_counts)

    return render(request, 'recipes/charts.html', {
        'difficulty_chart': difficulty_chart
    })

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('recipes:recipe_details')  # Or wherever you want to send users after
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})

@login_required
def about(request):
    return render(request, 'recipes/about.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after signup
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})