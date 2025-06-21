from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('login') 
        self.login_url = reverse('login')
        self.username = 'testuser'
        self.password = 'securepass123'

    def test_signup_form_valid(self):
        response = self.client.post(self.signup_url, {
            'username': self.username,
            'password1': self.password,
            'password2': self.password,
            'signup': ''  # triggers signup path
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_signup_form_invalid_password_mismatch(self):
        response = self.client.post(self.signup_url, {
            'username': 'wronguser',
            'password1': 'abc123',
            'password2': 'different123',
            'signup': ''
        })
        self.assertContains(response, 'Signup failed', status_code=200)

    def test_login_valid_credentials(self):
        # Create the user
        User.objects.create_user(username=self.username, password=self.password)

        # Try logging in
        response = self.client.post(self.login_url, {
            'username': self.username,
            'password': self.password,
            'login': ''
        })
        self.assertEqual(response.status_code, 302)  # redirect on success

    def test_login_invalid_credentials(self):
        response = self.client.post(self.login_url, {
            'username': 'nonexistent',
            'password': 'wrongpass',
            'login': ''
        })
        self.assertContains(response, 'Invalid login', status_code=200)