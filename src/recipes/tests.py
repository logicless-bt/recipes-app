from django.test import TestCase
from.models import Recipe

# Create your tests here.
class RecipeModelTest(TestCase):
    def setUpTestData():
        Recipe.objects.create(name='Slop', ingredients = "Grits, milk, oats, water", cooking_time = 5)
    
    def test_recipe_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('name').max_length

        self.assertEqual(max_length, 120)

    def test_recipe_name(self):
        recipe = Recipe.objects.get(id=1)
        label = recipe._meta.get_field('name').verbose_name
        self.assertEqual(label, 'name')