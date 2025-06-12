from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.conf import settings
from .models import Recipe
from .forms import RecipeSearchForm

# Create your tests here.
class RecipeModelTest(TestCase):
    def setUpTestData():
        Recipe.objects.create(name='Slop', ingredients = "Grits, milk, oats, water", cooking_time = 5)
   
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
    
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
        # Check that the response contains a link to login
        login_url = reverse('login')
        self.assertContains(response, f'href="{login_url}"')

    def test_recipe_details_info(self):
        self.client.login(username='testuser', password='testpass')
        recipe1 = Recipe.objects.get(id=1)
        response = self.client.get(reverse('recipes:recipe_details'))
        self.assertEqual(response.status_code, 200)

        # Check that the recipe name, description, cooking_time, difficulty appear in the response
        self.assertContains(response, recipe1.name)
        self.assertContains(response, recipe1.description)
        self.assertContains(response, str(recipe1.cooking_time))
    
    def test_recipe_images(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('recipes:recipe_details'))
        self.assertEqual(response.status_code, 200)

        recipes = Recipe.objects.all()
        for recipe in recipes:
            self.assertContains(response, recipe.pic.url)

class RecipeFormTest(TestCase):
    def test_valid_form_data(self):
        form_data = {
            'recipe_name': 'Pasta',
            'chart_type': '#2'
        }
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_data(self):
        form_data = {
            'recipe_name': '',  # Required field left blank
            'chart_type': 'invalid_type'
        }
        form = RecipeSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

class RecipeViewProtectionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.recipe = Recipe.objects.create(
            name='Pizza',
            description='Cheesy goodness',
            ingredients='cheese, dough, tomato',
            cooking_time=20
        )
        self.recipe.calculate_difficulty()

    def test_recipe_details_requires_login(self):
        response = self.client.get(reverse('recipes:recipe_details'))
        self.assertRedirects(response, f'{settings.LOGIN_URL}?next={reverse("recipes:recipe_details")}')
