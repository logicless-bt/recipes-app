from django.urls import path
from . import views

#setting the 'home' path to be the default
app_name = 'recipes'
urlpatterns = [
    path('', views.recipe_details, name = 'recipe_details'),
    path('<int:pk>/', views.recipe_indiv, name='recipe_indiv'),
    path('search', views.search, name="search")
]