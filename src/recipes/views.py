from django.shortcuts import render, get_object_or_404
from .models import Recipe
from .forms import RecipeSearchForm
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
    #create instance of RecipeSearchForm
    form = RecipeSearchForm(request.POST or None)
    recipe_df = None
    recipe_name = None
    chart = None
    if request.method =='POST':
       #read recipe_name and chart_type
       recipe_name = request.POST.get('recipe_name')
       chart_type = request.POST.get('chart_type')
       #apply filter to extract data
       qs = Recipe.objects.filter(name=recipe_name)
       if qs:      #if data found
           #convert the queryset values to pandas dataframe
           recipe_df=pd.DataFrame(qs.values()) 
           #convert ID to name
           recipe_df['id']=recipe_df['id'].apply(get_recipename_from_id)
           #convert to HTML
           recipe_df=recipe_df.to_html()

           chart=get_chart(chart_type, recipe_df, labels=recipe_df['date_created'].values)
       #debugging
       print (recipe_name, chart_type)
    print ('Exploring querysets:')
    print ('Case 1: Output of Recipe.objects.all()')
    qs=Recipe.objects.all()
    print (qs)

    print ('Case 2: Output of Recipe.objects.filter(recipe__name=recipe_name)')
    qs = Recipe.objects.filter(name = recipe_name)
    print (qs)

    print ('Case 3: Output of qs.values')
    print (qs.values())

    print ('Case 4: Output of qs.values_list()')
    print (qs.values_list())

    print ('Case 5: Output of Recipe.objects.get(id=1)')
    obj = Recipe.objects.get(id=1)
    print (obj)
    #transfer data
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

    # Recipe over time
    recipe_dates = pd.to_datetime([r.date_created for r in recipes])
    recipe_counts = pd.Series(1, index=recipe_dates).resample('M').sum()

    # Generate charts
    difficulty_chart = get_chart('pie', difficulty_counts)
    line_chart = get_chart('line', recipe_counts)

    return render(request, 'recipes/charts.html', {
        'difficulty_chart': difficulty_chart,
        'line_chart': line_chart,
    })