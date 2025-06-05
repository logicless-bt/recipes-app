from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
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
    
    def test_home_page_link(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        # Check that the response contains a link to recipe_details URL
        recipe_details_url = reverse('recipes:recipe_details')
        self.assertContains(response, f'href="{recipe_details_url}"')

    def test_recipe_details_info(self):
        recipe1 = Recipe.objects.get(id=1)
        response = self.client.get(reverse('recipes:recipe_details'))
        self.assertEqual(response.status_code, 200)

        # Check that the recipe name, description, cooking_time, difficulty appear in the response
        self.assertContains(response, recipe1.name)
        self.assertContains(response, recipe1.description)
        self.assertContains(response, str(recipe1.cooking_time))
        self.assertContains(response, recipe1.difficulty)
    
    def test_recipe_images(self):
        response = self.client.get(reverse('recipes:recipe_details'))
        self.assertEqual(response.status_code, 200)

        recipes = Recipe.objects.all()
        for recipe in recipes:
            self.assertContains(response, recipe.pic.url)