from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from user_auth_app.models import UserProfile


class UserRegisterViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-register')

    def test_register_user_success(self):
        data = {
            'username': 'newuser',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'phone_number': '1234567890',
            'color': 'blue'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertEqual(response.data['email'], 'newuser@example.com')

    def test_register_user_missing_fields(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.data)
        self.assertEqual(
            response.data['message'], 'Username, email, and password are required.')

    def test_register_user_existing_username(self):
        User.objects.create_user(
            username='existinguser', email='existinguser@example.com', password='password')
        data = {
            'username': 'existinguser',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'phone_number': '1234567890',
            'color': 'blue'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Username already exists.')

    def test_register_user_existing_email(self):
        User.objects.create_user(
            username='user1', email='existingemail@example.com', password='password')
        data = {
            'username': 'newuser',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'existingemail@example.com',
            'password': 'newpassword',
            'phone_number': '1234567890',
            'color': 'blue'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Email already exists.')
