from django.urls import path
from .views import home

#setting the 'home' path to be the default
app_name = 'recipes'
urlpatterns = [
    path('', home)
]