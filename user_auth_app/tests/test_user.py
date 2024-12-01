
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url_list = reverse('user-list')
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_users(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)

    def test_create_user_success(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'phone_number': '1234567890',
            'color': 'blue'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('token', response.data['data'])
        self.assertEqual(response.data['data']['username'], 'newuser')
        self.assertEqual(response.data['data']['email'], 'newuser@example.com')

    def test_create_user_missing_fields(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Username, email, and password are required.')

    def test_create_user_existing_username(self):
        User.objects.create_user(
            username='existinguser', email='existinguser@example.com', password='password')
        data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
            'phone_number': '1234567890',
            'color': 'blue'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Username already exists.')