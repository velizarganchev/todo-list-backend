from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserLoginViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('user-login')
        self.user = User.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_login_user_success(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['email'], 'testuser@example.com')

    def test_login_user_invalid_credentials(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Invalid credentials.')

    def test_login_user_nonexistent_email(self):
        data = {
            'email': 'nonexistent@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'User with this email does not exist.')

    def test_login_user_missing_fields(self):
        data = {
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Email and password are required.')
